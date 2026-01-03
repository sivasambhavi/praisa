from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Database setup
DATABASE_URL = "sqlite:///praisa_demo.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_patient(patient_id: str):
    """Get patient by ID"""
    with get_db() as db:
        query = text("SELECT * FROM patients WHERE patient_id = :pid")
        result = db.execute(query, {"pid": patient_id}).mappings().first()
        if result:
            return dict(result)
        return None

def search_patients(name: str = None, abha: str = None):
    """Search patients by name (partial) or ABHA (exact)"""
    with get_db() as db:
        if abha:
            query = text("SELECT * FROM patients WHERE abha_number = :abha")
            results = db.execute(query, {"abha": abha}).mappings().all()
        elif name:
            # Case insensitive search
            query = text("SELECT * FROM patients WHERE lower(name) LIKE :name LIMIT 10")
            results = db.execute(query, {"name": f"%{name.lower()}%"}).mappings().all()
        else:
            return []
            
        return [dict(row) for row in results]

def get_patient_visits(patient_id: str):
    """Get all visits for a patient"""
    with get_db() as db:
        query = text("""
            SELECT * FROM visits 
            WHERE patient_id = :pid 
            ORDER BY admission_date DESC
        """)
        results = db.execute(query, {"pid": patient_id}).mappings().all()
        return [dict(row) for row in results]
