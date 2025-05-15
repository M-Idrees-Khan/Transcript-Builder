import sqlite3

def connect_db():
    conn = sqlite3.connect("transcript.db")
    return conn

# Create required tables if they don't exist
def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    # Create students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT NOT NULL,
        roll_no TEXT NOT NULL UNIQUE
    )
    """)

    # Create subjects table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        semester INTEGER,
        subject_name TEXT,
        marks INTEGER,
        FOREIGN KEY (student_id) REFERENCES students(id)
    )
    """)

    conn.commit()
    conn.close()
