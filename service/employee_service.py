from database.db import get_db_connection

def find_employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    conn.close()

    employee_list = []
    for employee in employees:
        employee_list.append({
            'id': employee['id'],
            'name': employee['name'],
            'role': employee['role']
        })

    return employee_list