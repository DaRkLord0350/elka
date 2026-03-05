from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import requests
import os
from pathlib import Path

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
DOC_DIR = "data/documents"

# Ensure documents directory exists
Path(DOC_DIR).mkdir(parents=True, exist_ok=True)


def download_drive_files(service_account_file, folder_id):
    """
    Download files from a Google Drive folder
    
    Args:
        service_account_file: Path to service account JSON file
        folder_id: Google Drive folder ID
        
    Returns:
        List of downloaded file paths
    """
    try:
        # Check if service account file exists
        if not os.path.exists(service_account_file):
            raise FileNotFoundError(
                f"Service account file not found: {service_account_file}\n"
                f"Please provide a valid service account JSON in the credentials."
            )
        
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
        print(f"Found {len(files)} files in Google Drive folder")

        downloaded = []

        for file in files:
            try:
                request = service.files().get_media(fileId=file["id"])
                path = f"{DOC_DIR}/{file['name']}"

                with open(path, "wb") as f:
                    f.write(request.execute())

                downloaded.append(path)
                print(f"✓ Downloaded: {file['name']}")
            except Exception as e:
                print(f"✗ Failed to download {file['name']}: {str(e)}")
                continue

        print(f"Successfully downloaded {len(downloaded)} files")
        return downloaded
        
    except FileNotFoundError as fe:
        print(f"Error: {str(fe)}")
        raise
    except Exception as e:
        print(f"Error accessing Google Drive: {str(e)}")
        raise