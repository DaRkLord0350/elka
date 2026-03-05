from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import requests
import os

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def download_drive_files(service_account_file, folder_id):

    creds = Credentials.from_service_account_file(
        service_account_file,
        scopes=SCOPES
    )

    service = build("drive", "v3", credentials=creds)

    results = service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=50,
        fields="files(id, name)"
    ).execute()

    files = results.get("files", [])

    downloaded = []

    for file in files:

        request = service.files().get_media(fileId=file["id"])

        path = f"data/documents/{file['name']}"

        with open(path, "wb") as f:
            f.write(request.execute())

        downloaded.append(path)

    return downloaded