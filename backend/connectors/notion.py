from notion_client import Client
import os


def fetch_notion_pages(token, database_id):

    notion = Client(auth=token)

    pages = notion.databases.query(database_id=database_id)

    texts = []

    for page in pages["results"]:

        title = page["properties"]["Name"]["title"][0]["text"]["content"]

        texts.append(title)

    path = "data/documents/notion_export.txt"

    with open(path, "w") as f:
        f.write("\n".join(texts))

    return path