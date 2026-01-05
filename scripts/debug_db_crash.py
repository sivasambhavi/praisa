
import sys
import os
from sqlalchemy import text  # Add this import

# Add the project root to sys.path so we can import app modules
sys.path.append(os.getcwd())

try:
    from app.database import db
    print("Successfully imported app.database.db")
except Exception as e:
    print(f"Failed to import app.database.db: {e}")
    sys.exit(1)

def test_crash():
    print("Testing search_patients with name='Ramesh'...")
    try:
        # DB connection check
        with db.get_db() as session:
            print("DB connection successful.")
            try:
                # Basic query to verify table existence
                session.execute(text("SELECT 1 FROM patients"))
                print("Table check passed.")
            except Exception as e:
                print(f"Table check failed: {e}")

        results = db.search_patients(name="Ramesh")
        print(f"Results: {len(results)}")
        for r in results:
            print(r)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_crash()
