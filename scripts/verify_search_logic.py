
import sys
import os
from sqlalchemy import text

sys.path.append(os.getcwd())
from app.database import db

def check_data_and_search():
    try:
        with db.get_db() as session:
            # 1. Get sample data
            print("--- Sample Patients ---")
            query = text("SELECT id, name, aadhaar_number, mobile FROM patients LIMIT 5")
            rows = session.execute(query).mappings().all()
            if not rows:
                print("No patients found in DB despite loader success!")
                return
            
            for row in rows:
                print(dict(row))
                
            sample_person = rows[0]
            name = sample_person['name']
            aadhaar = sample_person['aadhaar_number']
            
            print(f"\n--- Testing Search for: '{name}' ---")
            results = db.search_patients(name=name)
            print(f"Found: {len(results)}")
            
            if aadhaar:
                print(f"\n--- Testing Search for Aadhaar: '{aadhaar}' ---")
                results_aadhaar = db.search_patients(aadhaar=aadhaar)
                print(f"Found: {len(results_aadhaar)}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_data_and_search()
