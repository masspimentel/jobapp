from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import streamlit as st
import json

def log_to_sheets(sheet_id, values):
    """
    Logs values to a Google Sheets document.

    Args:
        sheet_id (str): The ID of the Google Sheets document.
        values (list): A list of lists containing the values to log.
    """
    creds_json = st.secrets.get("GOOGLE_SERVICE_ACCOUNT")
    creds_dict = json.loads(creds_json) if creds_json else None
    if not creds_dict:
        st.error("Google service account credentials not found in secrets.")
        return None
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    
    service = build("sheets", "v4", credentials=creds)
    
    body = {
        "values": values
    }
    
    try:
        service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range="Sheet1!A1",
            valueInputOption="RAW",
            body=body
        ).execute()
    except HttpError as err:
        print(f"An error occurred: {err}")