from datetime import datetime
from database.db import get_db_connection
from enums.education_form import EducationForm
from model.student_info import StudentInfo
from service.html_parser_service import get_program_url

def find_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM conversations')
    conversations = cursor.fetchall()
    conn.close()

    conversations_list = []
    for conversation in conversations:
        conversations_list.append({
            'user_id': conversation['user_id'],
            'sender': conversation['sender'],
            'message': conversation['message'],
            'timestamp' : conversation['timestamp']
        })

    return conversations_list


def get_link_of_schedule_by_faculty_number(faculty_number):
    student_info = get_student_faculty_info(faculty_number)
    print(student_info)
    return get_program_url(student_info)


def get_student_faculty_info(faculty_number):
    if not faculty_number.isdigit():
        return
    major_code = int(faculty_number[4:6])
    education_form_code = int(faculty_number[6:7])
    major = StudentInfo.get_major_by_code(major_code)
    university_year = (datetime.now().year % 100) - int(faculty_number[0:2])
    education_form = EducationForm.REGULAR if education_form_code == 1 else EducationForm.ABSENTIA
    return StudentInfo(major, education_form, university_year)
