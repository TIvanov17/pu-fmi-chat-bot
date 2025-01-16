import datetime
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('schema.database')
    conn.row_factory = sqlite3.Row
    conn.text_factory = str
    return conn

def insert_conversation(sid, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations (user_id, sender, message, timestamp) VALUES (?, ?, ?, ?)",
                   (sid, "system", message, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

def get_last_conversation_message(sid):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
               SELECT message FROM conversations 
               WHERE user_id = ? ORDER BY id DESC LIMIT 1 OFFSET 1
           """, (sid,))
    last_message = cursor.fetchone()
    return last_message

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

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                sender TEXT,
                message TEXT,
                timestamp TEXT
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
