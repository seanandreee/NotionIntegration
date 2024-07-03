import requests
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
load_dotenv("api.env")

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID2 = os.getenv('DATABASE_ID2')

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}
def get_pages(num_pages=None):

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID2}/query"

    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    # Comment this out to dump all data to a file
    import json
    with open('db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    return results
pages = get_pages()  # I'm assuming this returns the list of pages as dictionaries

# Sort pages by 'Launch Date'; handling None dates by placing them last
sorted_pages = sorted(pages, key=lambda x: (x["properties"]["Launch Date"]["date"] is None, x["properties"]["Launch Date"]["date"]["start"] if x["properties"]["Launch Date"]["date"] is not None else ''))

for page in sorted_pages:
    # Extract properties as before
    page_type = page["properties"]["Type"]["select"]["name"]
    status = page["properties"]["Status"]["select"]["name"]
    name = page["properties"]["Name"]["title"][0]["plain_text"]
    grade_options = page["properties"]["Grade"]["multi_select"]
    grades = [option["name"] for option in grade_options]
    launch_date = page["properties"]["Launch Date"]["date"]
    if launch_date is not None:
        launch_date = launch_date["start"]
    else:
        launch_date = "No date"

    # Print out or process these properties
    print(f"Type: {page_type}, Status: {status}, Name: {name}, Grades: {', '.join(grades)}, Launch Date: {launch_date}")
