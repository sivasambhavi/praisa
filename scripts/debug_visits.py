
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///praisa_demo.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def check_visits():
    db = SessionLocal()
    try:
        # Check count of visits
        print("Checking 'visits' table...")
        res = db.execute(text("SELECT COUNT(*) as count FROM visits")).mappings().first()
        print(f"Total Visits in DB: {res['count']}")
        
        if res['count'] > 0:
            # Show a sample
            sample = db.execute(text("SELECT * FROM visits LIMIT 5")).mappings().all()
            print("\nSample Visits:")
            for v in sample:
                print(v)
        else:
            print("❌ No visits found! This explains the blank history.")

    except Exception as e:
        print(f"❌ DB Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_visits()
