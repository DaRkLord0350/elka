import subprocess

from backend.connectors.google_drive import download_drive_files
from backend.connectors.slack import fetch_slack_messages
from backend.connectors.notion import fetch_notion_pages


def run_sync():

    print("Starting external knowledge sync...")

    # Google Drive
    download_drive_files(
        "service_account.json",
        "GOOGLE_FOLDER_ID"
    )

    # Slack
    fetch_slack_messages(
        "SLACK_BOT_TOKEN",
        "CHANNEL_ID"
    )

    # Notion
    fetch_notion_pages(
        "NOTION_TOKEN",
        "DATABASE_ID"
    )

    print("Running ingestion pipeline...")

    subprocess.run(["python", "run_ingestion.py"])

    print("Sync completed.")