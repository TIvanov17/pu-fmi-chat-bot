import sqlite3

def get_db_connection():
    conn = sqlite3.connect('schema.database')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
           CREATE TABLE IF NOT EXISTS employees (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               role TEXT NOT NULL
           )
       ''')

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
