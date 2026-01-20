import streamlit as st
import datetime
import os
from googleapiclient.discovery import build
import auth
import styles
import calendar_view

# ---------------------------------------------------------
# Minimalist Config
# ---------------------------------------------------------
st.set_page_config(page_title="Shift Tool", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# Apply Mobile Styles
st.markdown(styles.get_mobile_css(), unsafe_allow_html=True)

SHIFT_SLOTS = {
    "Yコマ": {"start": "10:20", "end": "11:50"},
    "休憩 (45分)": {"start": "11:50", "end": "12:35"},
    "Zコマ": {"start": "12:35", "end": "14:05"},
    "Aコマ": {"start": "14:10", "end": "15:40"},
    "休憩 (60分)": {"start": "15:40", "end": "16:40"},
    "Bコマ": {"start": "16:40", "end": "18:10"},
    "Cコマ": {"start": "18:15", "end": "19:45"},
    "Dコマ": {"start": "19:50", "end": "21:20"},
}

def main():
    # ---------------------------------------------------------
    # Auth & Setup
    # ---------------------------------------------------------
    creds = auth.authenticate_google_calendar()
    if not creds:
        st.warning("🔑 Login required")
        return

    service = build("calendar", "v3", credentials=creds)

    # ---------------------------------------------------------
    # UI: Header & Calendar
    # ---------------------------------------------------------
    c1, c2 = st.columns([2, 3])
    with c1:
        st.title("⚡ Shift")
    with c2:
        try:
            calendars = service.calendarList().list().execute().get("items", [])
            opts = {c["summary"]: c["id"] for c in calendars}
            
            # Prioritize "61_Meiko Gijuku"
            default_ix = 0
            keys = list(opts.keys())
            target_cal = "61_Meiko Gijuku"
            if target_cal in keys:
                default_ix = keys.index(target_cal)
            
            cal_name = st.selectbox("Calendar", keys, index=default_ix, label_visibility="collapsed")
            cal_id = opts[cal_name]
        except:
            st.error("Calendar Error")
            return

    st.divider()

    # ---------------------------------------------------------
    # UI: Calendar View (Replaces Date Controller)
    # ---------------------------------------------------------
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = datetime.date.today()

    # Render Custom Calendar
    calendar_view.render_calendar(service, cal_id)
    
    # ---------------------------------------------------------
    # UI: Selected Date Actions
    # ---------------------------------------------------------
    st.divider()
    selected = st.session_state.selected_date
    st.subheader(f"📝 {selected.strftime('%m/%d (%a)')}")
    
    # 1. Action Grid (Register Shifts)
    keys = list(SHIFT_SLOTS.keys())
    pairs = [keys[i:i+2] for i in range(0, len(keys), 2)]
    
    for pair in pairs:
        cols = st.columns(2)
        for i, key in enumerate(pair):
            slot = SHIFT_SLOTS[key]
            with cols[i]:
                # Simply Label: "Aコマ"
                if st.button(key, key=f"btn_{key}", use_container_width=True):
                    add_shift(service, cal_id, selected, key, slot)

    # 2. Existing List (Delete)
    st.caption("Registered Shifts")
    events = list_events(service, cal_id, selected)
    
    if events:
        for e in events:
            start = e['start'].get('dateTime', e['start'].get('date'))[11:16]
            end = e['end'].get('dateTime', e['end'].get('date'))[11:16]
            summary = e.get('summary', '?')
            evt_id = e['id']
            
            # Card style for deletion
            with st.container():
                ec1, ec2 = st.columns([4, 1])
                with ec1:
                    st.markdown(f"**{summary}** <span style='color:#888'>({start}-{end})</span>", unsafe_allow_html=True)
                with ec2:
                    if st.button("✕", key=f"del_{evt_id}"):
                        delete_event(service, cal_id, evt_id)
                        st.rerun()
                st.markdown("<hr style='margin:0.5em 0; opacity:0.3'>", unsafe_allow_html=True)
    else:
        st.info("No shifts for this day.")

    # ---------------------------------------------------------
    # Logs (Hidden)
    # ---------------------------------------------------------
    with st.expander("Debug Logs"):
        if st.button("Clear Log"):
            st.session_state.logs = []
            st.rerun()
        if "logs" in st.session_state:
             st.write(st.session_state.logs)

# ---------------------------------------------------------
# Logic Functions
# ---------------------------------------------------------
def list_events(service, calendar_id, date):
    try:
        t_min = f"{date.strftime('%Y-%m-%d')}T00:00:00+09:00"
        t_max = f"{date.strftime('%Y-%m-%d')}T23:59:59+09:00"
        res = service.events().list(calendarId=calendar_id, timeMin=t_min, timeMax=t_max, singleEvents=True, orderBy='startTime').execute()
        return res.get('items', [])
    except: return []

def delete_event(service, cal_id, evt_id):
    try:
        service.events().delete(calendarId=cal_id, eventId=evt_id).execute()
        st.toast("Deleted schedule", icon="🗑️")
    except: pass

def add_shift(service, cal_id, date, summary, slot):
    try:
        start = f"{date.strftime('%Y-%m-%d')}T{slot['start']}:00"
        end = f"{date.strftime('%Y-%m-%d')}T{slot['end']}:00"
        body = {
            'summary': summary,
            'start': {'dateTime': start, 'timeZone': 'Asia/Tokyo'},
            'end': {'dateTime': end, 'timeZone': 'Asia/Tokyo'}
        }
        res = service.events().insert(calendarId=cal_id, body=body).execute()
        st.toast(f"Added: {summary}", icon="✅")
        
        if "logs" not in st.session_state: st.session_state.logs = []
        st.session_state.logs.append({"Action": "Insert", "Summary": summary, "Res": res})
        
        # Rerun to update calendar view immediately
        st.rerun()
    except Exception as e:
        st.error(str(e))

if __name__ == "__main__":
    main()
