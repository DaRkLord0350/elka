from slack_sdk import WebClient
import os


def fetch_slack_messages(token, channel_id):

    client = WebClient(token=token)

    response = client.conversations_history(
        channel=channel_id,
        limit=100
    )

    messages = response["messages"]

    text_data = []

    for msg in messages:

        if "text" in msg:
            text_data.append(msg["text"])

    file_path = "data/documents/slack_channel.txt"

    with open(file_path, "w") as f:
        f.write("\n".join(text_data))

    return file_path