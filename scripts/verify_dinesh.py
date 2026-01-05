
import sys
import os
from sqlalchemy import text

sys.path.append(os.getcwd())
from app.database import db

def verify_match_candidates():
    print("Searching for 'Dinesh'...")
    # Search without hospital_id to get global results (or simulates it)
    # Actually, the API usually searches within a hospital, then matching happens across.
    # But let's seeing if both exist in DB.
    
    with db.get_db() as session:
        results = session.execute(text("SELECT id, hospital_id, name, mobile, aadhaar_number FROM patients WHERE name LIKE '%Dinesh%'")).mappings().all()
        
        print(f"Found {len(results)} patients named Dinesh:")
        for r in results:
            print(dict(r))

if __name__ == "__main__":
    verify_match_candidates()
