from slack_sdk import WebClient
import os
from pathlib import Path

DOC_DIR = "data/documents"
Path(DOC_DIR).mkdir(parents=True, exist_ok=True)


def fetch_slack_messages(token, channel_id):
    """
    Fetch messages from a Slack channel
    
    Args:
        token: Slack Bot User OAuth Token
        channel_id: Slack channel ID
        
    Returns:
        Path to file containing channel messages
    """
    try:
        client = WebClient(token=token)

        response = client.conversations_history(
            channel=channel_id,
            limit=100
        )

        messages = response["messages"]
        print(f"Fetched {len(messages)} messages from Slack channel")

        text_data = []

        for msg in messages:
            if "text" in msg:
                text_data.append(msg["text"])

        file_path = f"{DOC_DIR}/slack_channel_{channel_id}.txt"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(text_data))

        print(f"✓ Saved {len(text_data)} messages to {file_path}")
        return file_path
        
    except Exception as e:
        print(f"Error fetching Slack messages: {str(e)}")
        raise