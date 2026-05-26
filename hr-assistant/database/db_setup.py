import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "hr_database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Employees Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Leave Requests Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            days INTEGER,
            reason TEXT,
            status TEXT DEFAULT 'Pending'
        )
    ''')

    # HR Tickets Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT CHECK(category IN ('payroll', 'technical', 'leave', 'onboarding')),
            issue TEXT,
            status TEXT DEFAULT 'Open'
        )
    ''')

    # Interviews Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            scheduled_time TEXT,
            status TEXT DEFAULT 'Scheduled'
        )
    ''')

    conn.commit()
    conn.close()

def execute_query(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    result = cursor.fetchall()
    conn.close()
    return result

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")