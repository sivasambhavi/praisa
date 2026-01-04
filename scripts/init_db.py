import sqlite3
import os

DB_FILE = "praisa_demo.db"
SCHEMA_FILE = "app/database/schema.sql"

def init_db():
    print(f"Initializing {DB_FILE}...")
    
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
            print("Removed existing DB.")
        except:
            pass

    with open(SCHEMA_FILE, 'r') as f:
        schema = f.read()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
