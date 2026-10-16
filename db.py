import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = BASE_DIR / "database.db"
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL ,
                    service TEXT NOT NULL,
                    condition TEXT NOT NULL,
                    acreage REAL NOT NULL,
                    low REAL ,
                    high REAL ,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP )""")
    conn.commit()
    conn.close()

def insert_lead(email,service,condition,acreage,low,high):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO leads (email,service,condition,acreage,low,high) VALUES (?, ?, ?, ?, ?, ?)", (email,service,condition,acreage,low,high))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception:
        return False
    finally:
        conn.close()

def get_lead(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads WHERE email = (?)", (email,))
    result = cursor.fetchall()
    conn.close()
    return result

def get_lead_heavy():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads WHERE condition = (?)", ("heavy",))
    result = cursor.fetchall()
    conn.close()
    return result
