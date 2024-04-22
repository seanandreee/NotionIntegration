import requests
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
load_dotenv("api.env")

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID3 = os.getenv('DATABASE_ID3')

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}
def get_pages(num_pages=None):

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID3}/query"

    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    # Comment this out to dump all data to a file
    import json
    with open('db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    return results


def student_extract(pages): #extracts metadata from student pages (name, grade)
    students_info = []
    for page in pages:
        # Extract properties as before
        student_page_id = page['id']
        status = page["properties"]["Status"]["select"]["name"]
        student_name = page["properties"]["Name"]["title"][0]["plain_text"]
        
        # If 'Grade' is a single select property
        grade = page["properties"]["Grade"]["select"]["name"]  # Directly get the 'name' from the 'select'

        # Print out or process these properties
        students_info.append({"name": student_name, "grade": grade, "page id": student_page_id}) # shape of your data


        # print(f"Status: {status}, Name: {student_name}, Grade: {grade}")

    return students_info #returns package

'''
def run_students():
    pages = get_pages()  # I'm assuming this returns the list of pages as dictionaries
    return student_extract(pages)

#print(student_extract(pages))'''

pages = get_pages()

student_data = student_extract(pages)
#print(student_data)