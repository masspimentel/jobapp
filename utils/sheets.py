from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

def log_to_sheets(sheet_id, values):
    """
    Logs values to a Google Sheets document.

    Args:
        sheet_id (str): The ID of the Google Sheets document.
        values (list): A list of lists containing the values to log.
    """
    creds = service_account.Credentials.from_service_account_file(
        "service_account.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
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