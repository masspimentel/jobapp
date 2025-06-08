from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_drive(file_path, name):
    creds = service_account.Credentials.from_service_account_file(
        "service_account.json",
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    service = build("drive", "v3", credentials=creds)

    metadata = {"name": name}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=metadata, media_body=media, fields="id").execute()
    return file.get("id")