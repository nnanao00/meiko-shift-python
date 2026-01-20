import streamlit as st
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def authenticate_google_calendar():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    elif "google_token" in st.secrets:
        creds = Credentials.from_authorized_user_info(st.secrets["google_token"], SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                st.error(f"認証の更新に失敗しました: {e}")
                return None
        else:
            if "google_token" in st.secrets:
                return None
            if not os.path.exists("credentials.json"):
                return None
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            except Exception as e:
                st.error(f"認証に失敗しました: {e}")
                return None
        
        try:
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        except:
            pass
            
    return creds
