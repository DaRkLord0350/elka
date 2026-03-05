from notion_client import Client
import os
from pathlib import Path

DOC_DIR = "data/documents"
Path(DOC_DIR).mkdir(parents=True, exist_ok=True)


def fetch_notion_pages(token, database_id):
    """
    Fetch pages from a Notion database
    
    Args:
        token: Notion Internal Integration Token
        database_id: Notion database ID
        
    Returns:
        Path to file containing database content
    """
    try:
        notion = Client(auth=token)

        pages = notion.databases.query(database_id=database_id)
        print(f"Fetched {len(pages['results'])} pages from Notion database")

        texts = []

        for page in pages["results"]:
            try:
                # Try to get the title from the Name property
                title = page["properties"]["Name"]["title"][0]["text"]["content"]
                texts.append(title)
            except (KeyError, IndexError, TypeError):
                # If title doesn't exist, try to get page ID or skip
                print(f"⚠ Could not extract title from page {page['id']}")
                continue

        path = f"{DOC_DIR}/notion_export_{database_id}.txt"

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(texts))

        print(f"✓ Saved {len(texts)} pages to {path}")
        return path
        
    except Exception as e:
        print(f"Error fetching Notion pages: {str(e)}")
        raise