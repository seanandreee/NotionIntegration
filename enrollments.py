import requests
import os
from datetime import datetime, timezone
import modules
import students
import compare


from dotenv import load_dotenv
load_dotenv("api.env")

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID4 = os.getenv('DATABASE_ID4')

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}
def get_pages(num_pages=None):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID4}/query"

    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    # Comment this out to dump all data to a file
    import json
    with open('db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    results = data["results"]
    return results
    
pages = get_pages()

#INSERT PARSING LOGIC HERE

def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID4}, "properties": data}

    response = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)

    d = response.json()
    import json
    with open('db.json', 'w', encoding='utf8') as f:
        json.dump(d, f, ensure_ascii=False, indent=4)
    

    
    return d

for x in compare.relevant_students_and_modules:
    studentid = x[2]
    moduleid = x[4]
    #Name = (str(x[0]+x[3]))
    Name = (f"{x[0]} - {x[3]}")
    data = {
    "Status": {"select": {"name": "Active"}},
    "Name": {"title": [{"text": {"content": Name}}]},
    "📦 Test Module": {"relation": [{"id": moduleid}]},
    "🤔 Test Student": {"relation": [{"id": studentid}]},
    }
    
    create_page(data)

