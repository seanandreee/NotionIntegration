import requests
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import modules
import students
load_dotenv("api.env")

NOTION_TOKEN = os.getenv('NOTION_TOKEN')

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


published_date = datetime.now().astimezone(timezone.utc).isoformat()
current_date = datetime.today().date()  # Because 'datetime' now directly refers to the datetime class

#INSERT PARSING LOGIC HERE

#print(modules.module_data)
relevant_modules = []

def compare_dates():
    for x in modules.module_data:
        launch_date_str = x[5]
        if launch_date_str != 'No date':
        # Convert the launch date string to a date object
            launch_date_actual = datetime.strptime(launch_date_str, '%Y-%m-%d').date()
        
        # Compare the launch date to the current date
            if launch_date_actual == current_date:
                relevant_modules.append(x)

    return relevant_modules

extract_relevant_modules = compare_dates()
# if student grade == module grade: create string with student info and module info
def compare_grades():
    matched_students = set()  # Use a set to store unique student entries

    for x in extract_relevant_modules:
        applied_grade = x[4]
        for final_grade in applied_grade:            
            for y in students.student_data:
                testgrade = y["grade"]
                if testgrade == final_grade:
                    # Add a tuple representing the student to the set
                    matched_students.add((y["name"], y["grade"], y["page id"], x[3], x[0]))
    
    
    return matched_students

relevant_students_and_modules = compare_grades()
#print(extract_relevant_modules)
#print(relevant_students_and_modules)
