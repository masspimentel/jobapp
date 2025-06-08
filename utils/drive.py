from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import streamlit as st
import json

def upload_to_drive(file_path, name):
    creds_json = st.secrets.get("GOOGLE_SERVICE_ACCOUNT")
    creds_dict = json.loads(creds_json) if creds_json else None
    if not creds_dict:
        st.error("Google service account credentials not found in secrets.")
        return None
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    service = build("drive", "v3", credentials=creds)

    metadata = {"name": name}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=metadata, media_body=media, fields="id").execute()
    return file.get("id")