import sqlite3
from datetime import datetime

DB_FILE = 'fyndr.db'

def init_db():
    """Initialize the database and create necessary tables"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor() #cursor to execute SQL commands on each row
    
    # Create a table for storing user data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            file_name TEXT NOT NULL,
            saved_as TEXT NOT NULL,
            telegram_file_id TEXT NOT NULL,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    ''')

    # id - to identify each file uniquely
    # user_id - to identify the user who uploaded the file
    # file_name - original name of the file
    # saved_as - name of the file as saved in the system
    # telegram_file_id - unique identifier for the file in Telegram
    # upload_time - timestamp of when the file was uploaded
    
    conn.commit()
    conn.close()

    # insert the files to the table
def store_file(user_id, file_name, saved_as, telegram_file_id):
    """Insert a file record into the database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO files (user_id, file_name, saved_as, telegram_file_id)
        VALUES (?, ?, ?, ?)
    ''', (user_id, file_name, saved_as, telegram_file_id))
    
    conn.commit()
    conn.close()