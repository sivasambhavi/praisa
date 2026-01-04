"""
Database Access Layer for PRAISA

This module provides database connection management and query functions
for patient and visit data. Uses SQLAlchemy with raw SQL for simplicity.

Database: SQLite (POC) - Will migrate to PostgreSQL for production
ORM: SQLAlchemy with text() for raw SQL queries
Connection: Context manager pattern for automatic cleanup

Author: Mid Engineer
Date: 2026-01-04
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextmanager import contextmanager

# Database Configuration
# Using SQLite for POC demo - file-based database
# For production, this will be PostgreSQL connection string
DATABASE_URL = "sqlite:///praisa_demo.db"

# Create SQLAlchemy engine
# check_same_thread=False is required for SQLite to work with FastAPI
# (FastAPI uses multiple threads for async operations)
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # SQLite-specific setting
)

# Create session factory
# Sessions are used to interact with the database
# autocommit=False: Manual transaction control
# autoflush=False: Manual flush control
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    """
    Database session context manager.
    
    Provides a database session and ensures it's properly closed
    after use, even if an exception occurs.
    
    Usage:
        with get_db() as db:
            result = db.execute(query)
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()  # Create new session
    try:
        yield db  # Provide session to caller
    finally:
        db.close()  # Always close session (cleanup)


def get_patient(patient_id: str):
    """
    Get patient by unique patient ID.
    
    Retrieves a single patient record from the database by their
    unique patient_id (e.g., "HA001", "HB001").
    
    Args:
        patient_id: Unique patient identifier (e.g., "HA001")
    
    Returns:
        dict: Patient record with all fields, or None if not found
        
    Example:
        >>> get_patient("HA001")
        {'patient_id': 'HA001', 'name': 'Ramesh Singh', 'abha_number': '12-3456-7890-1234', ...}
    """
    with get_db() as db:
        # Use parameterized query to prevent SQL injection
        query = text("SELECT * FROM patients WHERE patient_id = :pid")
        
        # Execute query and get first result
        # mappings() converts Row objects to dict-like objects
        result = db.execute(query, {"pid": patient_id}).mappings().first()
        
        # Convert to regular dict if found, otherwise return None
        if result:
            return dict(result)
        return None


def search_patients(name: str = None, abha: str = None):
    """
    Search patients by name (partial match) or ABHA number (exact match).
    
    Supports two search modes:
    1. By ABHA number: Exact match on government health ID
    2. By name: Case-insensitive partial match (LIKE query)
    
    Args:
        name: Patient name to search (partial match, case-insensitive)
        abha: ABHA number to search (exact match)
    
    Returns:
        list[dict]: List of matching patient records (max 10 for name search)
        
    Examples:
        >>> search_patients(name="Ramesh")
        [{'patient_id': 'HA001', 'name': 'Ramesh Singh', ...}]
        
        >>> search_patients(abha="12-3456-7890-1234")
        [{'patient_id': 'HA001', ...}, {'patient_id': 'HB001', ...}]
    """
    with get_db() as db:
        if abha:
            # ABHA search: Exact match
            # Used when we have government health ID
            query = text("SELECT * FROM patients WHERE abha_number = :abha")
            results = db.execute(query, {"abha": abha}).mappings().all()
            
        elif name:
            # Name search: Case-insensitive partial match
            # LIKE query with wildcards for flexible matching
            # LIMIT 10 to prevent overwhelming results
            query = text("SELECT * FROM patients WHERE lower(name) LIKE :name LIMIT 10")
            results = db.execute(query, {"name": f"%{name.lower()}%"}).mappings().all()
            
        else:
            # No search criteria provided
            return []
        
        # Convert all results to regular dicts
        return [dict(row) for row in results]


def get_patient_visits(patient_id: str):
    """
    Get all visit records for a specific patient.
    
    Retrieves complete medical visit history for a patient,
    ordered by most recent first (descending admission date).
    
    Args:
        patient_id: Unique patient identifier (e.g., "HA001")
    
    Returns:
        list[dict]: List of visit records, newest first
        
    Example:
        >>> get_patient_visits("HA001")
        [
            {'visit_id': 'VA002', 'patient_id': 'HA001', 'admission_date': '2025-12-20', ...},
            {'visit_id': 'VA001', 'patient_id': 'HA001', 'admission_date': '2025-10-15', ...}
        ]
    """
    with get_db() as db:
        # Query all visits for this patient
        # ORDER BY admission_date DESC: Most recent visits first
        query = text("""
            SELECT * FROM visits 
            WHERE patient_id = :pid 
            ORDER BY admission_date DESC
        """)
        
        # Execute and convert results
        results = db.execute(query, {"pid": patient_id}).mappings().all()
        return [dict(row) for row in results]
