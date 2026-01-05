
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import datetime
import random

DATABASE_URL = "sqlite:///praisa_demo.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def seed_demo_visits():
    db = SessionLocal()
    try:
        print("Seeding demo visits for Ramesh (HA001) and Ramehs (HB001)...")
        
        visits = [
            # Hospital A - Source
            {
                "visit_id": "V_DEMO_01",
                "patient_id": "HA001",
                "visit_type": "OPD",
                "admission_date": "2025-12-15T10:30:00",
                "diagnosis": "Type 2 Diabetes Checkup",
                "doctor_name": "Dr. A. Sharma",
                "hospital_id": "hospital_a"
            },
            {
                "visit_id": "V_DEMO_02",
                "patient_id": "HA001",
                "visit_type": "LAB",
                "admission_date": "2025-11-20T09:00:00",
                "diagnosis": "Blood Sugar Test (HbA1c)",
                "doctor_name": "Dr. A. Sharma",
                "hospital_id": "hospital_a"
            },
            # Hospital B - Target (The 'Hidden' History)
            {
                "visit_id": "V_DEMO_03",
                "patient_id": "HB001",
                "visit_type": "EMERGENCY",
                "admission_date": "2025-12-28T22:15:00",
                "diagnosis": "Hypoglycemia (Low Blood Sugar)",
                "doctor_name": "Dr. B. Verma",
                "hospital_id": "hospital_b"
            },
            {
                "visit_id": "V_DEMO_04",
                "patient_id": "HB001",
                "visit_type": "PHARMACY",
                "admission_date": "2025-12-28T23:30:00",
                "diagnosis": "Insulin Dispensed",
                "doctor_name": "Pharmacist",
                "hospital_id": "hospital_b"
            }
        ]

        for v in visits:
            # Check if exists
            exists = db.execute(
                text("SELECT 1 FROM visits WHERE visit_id = :vid"), 
                {"vid": v["visit_id"]}
            ).scalar()
            
            if not exists:
                db.execute(
                    text("""
                        INSERT INTO visits (visit_id, patient_id, visit_type, admission_date, diagnosis, doctor_name, hospital_id)
                        VALUES (:visit_id, :patient_id, :visit_type, :admission_date, :diagnosis, :doctor_name, :hospital_id)
                    """),
                    v
                )
                print(f"Inserted {v['visit_id']}")
            else:
                print(f"Skipped {v['visit_id']} (Already exists)")
        
        db.commit()
        print("✅ Demo visits seeded successfully!")

    except Exception as e:
        print(f"❌ Error seeding visits: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_visits()
