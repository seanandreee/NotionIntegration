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
        launch_date_str = x[4]
        if launch_date_str != 'No date':
        # Convert the launch date string to a date object
            launch_date_actual = datetime.strptime(launch_date_str, '%Y-%m-%d').date()
        
        # Compare the launch date to the current date
            if launch_date_actual == current_date:
                relevant_modules.append(x)
    
    return relevant_modules

extract_relevant_modules = compare_dates()


def compare_grades():
    matched_students = set()  # Use a set to store unique student entries

    for x in extract_relevant_modules:
        applied_grade = x[3]
        for final_grade in applied_grade:            
            for y in students.student_data:
                testgrade = y["grade"]
                if testgrade == final_grade:
                    # Add a tuple representing the student to the set
                    matched_students.add((y["name"], y["grade"]))
    
    # After collecting all matches, print them out
        #print(f"Name: {student[0]}, Grade: {student[1]}")
    #print(matched_students)
    return matched_students

relevant_students = compare_grades()

print(relevant_students)