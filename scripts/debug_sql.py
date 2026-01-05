
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///praisa_demo.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def test_sql():
    db = SessionLocal()
    try:
        print("Testing basic query...")
        res = db.execute(text("SELECT name FROM patients LIMIT 1")).mappings().first()
        print(f"Basic Query OK: {res}")

        print("\nTesting REPLACE query...")
        abha = "12-3456-7890-1234"
        clean_abha = abha.replace("-", "").replace(" ", "").strip()
        
        sql = "SELECT * FROM patients WHERE REPLACE(REPLACE(abha_number, '-', ''), ' ', '') = :clean_abha"
        params = {"clean_abha": clean_abha}
        
        res = db.execute(text(sql), params).mappings().all()
        print(f"REPLACE Query OK: Found {len(res)} results")
        print(res)

    except Exception as e:
        print(f"\n❌ SQL Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_sql()
