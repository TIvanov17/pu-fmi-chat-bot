from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit
import eventlet  # Add this import for Eventlet
import sqlite3

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app)

def get_db_connection():
    conn = sqlite3.connect('schema.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

# Create table if it doesn't exist
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the employees table if it doesn't exist
    cursor.execute('''
           CREATE TABLE IF NOT EXISTS employees (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               role TEXT NOT NULL
           )
       ''')

    # Insert some initial data if the table is empty
    cursor.execute('SELECT COUNT(*) FROM employees')
    row = cursor.fetchone()
    if row[0] == 0:  # If no records exist, insert some initial data
        initial_data = [
            ('Alice', 'Manager'),
            ('Bob', 'Developer'),
            ('Charlie', 'Designer')
        ]
        cursor.executemany('INSERT INTO employees (name, role) VALUES (?, ?)', initial_data)
        conn.commit()  # Commit the transaction
    conn.close()

# @app.route('/')
# def home():
#     return render_template('index.html')
#

@app.route('/')
def index():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees').fetchall()
    conn.close()


    return render_template('index.html', employees=employees)


# API endpoint to get all employees
@app.route('/users', methods=['GET'])
def get_all_employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')  # Fetch all employees
    employees = cursor.fetchall()  # Get the result of the query
    conn.close()  # Close the connection

    # Convert rows to a list of dictionaries
    employee_list = []
    for employee in employees:
        employee_list.append({
            'id': employee['id'],
            'name': employee['name'],
            'role': employee['role']
        })

    return jsonify(employee_list)  # Return the employees in JSON format


@socketio.on('user_message')
def handle_user_message(message):
    print(f"User: {message}")
    emit('bot_reply', 'Hello, how can I assist you?')


if __name__ == '__main__':
    create_table()
    socketio.run(app, debug=True)
