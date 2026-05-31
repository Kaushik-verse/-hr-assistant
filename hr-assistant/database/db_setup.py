import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "hr_database.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, role TEXT NOT NULL)''')

    # UPDATED: Added start_date for conflict detection
    cursor.execute('''CREATE TABLE IF NOT EXISTS leaves (
        id INTEGER PRIMARY KEY AUTOINCREMENT, employee_name TEXT NOT NULL, start_date TEXT, days INTEGER, reason TEXT, status TEXT DEFAULT 'Pending')''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, issue TEXT, status TEXT DEFAULT 'Open')''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS interviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT, candidate_name TEXT, scheduled_time TEXT, status TEXT DEFAULT 'Scheduled')''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS performance_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT, employee_name TEXT, reviewer TEXT, rating INTEGER, comments TEXT)''')

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


def reset_db():
    """Drops all tables and recreates them for a fresh start."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = ['employees', 'leaves', 'tickets', 'interviews', 'performance_reviews']
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    conn.commit()
    conn.close()

    init_db()


if __name__ == "__main__":
    init_db()
