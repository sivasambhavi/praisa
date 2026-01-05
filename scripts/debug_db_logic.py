
from app.database.db import search_patients
from app.database import db

def debug_search(term):
    print(f"\n--- Debugging Search: '{term}' ---")
    
    # 1. Direct DB Query Check
    with db.get_db() as session:
        print("[SQL Check] Running raw LIKE query...")
        res = session.execute(db.text(f"SELECT * FROM patients WHERE lower(name) LIKE '%{term.lower()}%'")).mappings().all()
        print(f"[SQL Check] Found {len(res)} matches.")
        for r in res:
            print(f"  - {r['name']} ({r['hospital_id']})")

    # 2. Full Logic Check
    print("\n[Function Check] Running search_patients()...")
    results = search_patients(name=term)
    print(f"[Function Check] search_patients returned {len(results)} results.")
    for r in results:
        print(f"  - {r['name']} (Source: {r['hospital_id']})")

if __name__ == "__main__":
    debug_search("Ramesh") # Should fuzzy match "Ramehs"
    debug_search("Dinesh") # Should exact match "Dinesh"
