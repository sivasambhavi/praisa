
import sys
import os
from sqlalchemy import text

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.database import db

def check_db():
    print(f"Checking database at: {db.DATABASE_URL}")
    try:
        with db.get_db() as session:
            # List tables
            result = session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result.fetchall()]
            print(f"Tables found: {tables}")
            
            if 'patients' in tables:
                count = session.execute(text("SELECT count(*) FROM patients")).scalar()
                print(f"Patients count: {count}")
            else:
                print("Table 'patients' NOT found.")
                
    except Exception as e:
        print(f"Error checking DB: {e}")

if __name__ == "__main__":
    check_db()
