import streamlit as st
import datetime
import calendar
from dateutil.relativedelta import relativedelta

def get_month_events(service, calendar_id, year, month):
    """Fetch all events for the specified month to visualize them."""
    try:
        start_date = datetime.date(year, month, 1)
        end_date = start_date + relativedelta(months=1)
        
        t_min = f"{start_date.strftime('%Y-%m-%d')}T00:00:00+09:00"
        t_max = f"{end_date.strftime('%Y-%m-%d')}T00:00:00+09:00"
        
        events = service.events().list(
            calendarId=calendar_id,
            timeMin=t_min,
            timeMax=t_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        # Map date strings to event summaries
        # Format: "YYYY-MM-DD": ["Y", "45", "Z", "A"]
        event_map = {}
        for e in events.get('items', []):
            start = e['start'].get('dateTime', e['start'].get('date'))[:10]
            summary = e.get('summary', '??')
            if start not in event_map:
                event_map[start] = []
            
            # Abbreviate: "Aコマ" -> "A", "休憩 (45分)" -> "45"
            short = summary
            if "コマ" in summary:
                short = summary.replace("コマ", "")
            elif "休憩" in summary:
                if "45" in summary: short = "45"
                elif "60" in summary: short = "60"
                else: short = "休"
            
            event_map[start].append(short)
            
        return event_map
    except Exception as e:
        st.error(f"Calendar Fetch Error: {e}")
        return {}

def update_date(new_date):
    st.session_state.selected_date = new_date

def render_calendar(service, cal_id):
    """Renders a monthly calendar grid."""
    
    current_date = st.session_state.selected_date
    year = current_date.year
    month = current_date.month
    
    # --- Month Navigation ---
    c1, c2, c3 = st.columns([1, 10, 1]) # Wider center for desktop title
    with c1:
        if st.button("◀", key="prev_month"):
            st.session_state.selected_date = current_date - relativedelta(months=1)
            st.rerun()
    with c2:
        st.markdown(f"<h3 style='text-align: center; margin: 0;'>{year} / {month}</h3>", unsafe_allow_html=True)
    with c3:
        if st.button("▶", key="next_month"):
            st.session_state.selected_date = current_date + relativedelta(months=1)
            st.rerun()

    # --- Fetch Events ---
    event_map = get_month_events(service, cal_id, year, month)

    # --- Days Header ---
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    cols = st.columns(7)
    for i, d in enumerate(days):
        cols[i].markdown(f"<div style='text-align: center; color: #888; font-weight: bold; margin-bottom: 10px;'>{d}</div>", unsafe_allow_html=True)

    # --- Calendar Grid ---
    # Get matrix of days [ [0,0,1,2,3,4,5], [6,7,...] ]
    month_matrix = calendar.monthcalendar(year, month)
    
    for week in month_matrix:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("") # Empty cell
                continue
            
            this_date = datetime.date(year, month, day)
            date_str = this_date.strftime("%Y-%m-%d")
            
            # Button Label Logic
            label = str(day)
            
            # Check events
            if date_str in event_map:
                # Join all events together (compact)
                # e.g. ["Y", "45", "Z", "A"] -> "Y 45 Z A"
                shifts = " ".join(event_map[date_str])
                label += f"\n{shifts}"
            else:
                 # Minimal spacer to keep height consistent
                 label += "\n\n"
            
            # Style check
            is_selected = (this_date == current_date)
            # Use 'primary' for selected, but we rely on CSS to make sure content fits
            type_ = "primary" if is_selected else "secondary"
            
            # Render Button
            if cols[i].button(label, key=f"day_{year}_{month}_{day}", type=type_, use_container_width=True):
                 update_date(this_date)
                 st.rerun()
