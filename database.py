import sqlite3
import os
from config import DATABASE

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            semester INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            marks INTEGER NOT NULL,
            max_marks INTEGER DEFAULT 100,
            semester INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")