"""
Database Access Layer for PRAISA

This module provides database connection management and query functions
for patient and visit data. Uses SQLAlchemy with raw SQL for simplicity.

Database: SQLite (POC) - Will migrate to PostgreSQL for production
ORM: SQLAlchemy with text() for raw SQL queries
Connection: Context manager pattern for automatic cleanup
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from rapidfuzz import process, fuzz

# Database Configuration
# Using SQLite for POC demo - file-based database
# For production, this will be PostgreSQL connection string
# Use absolute path to avoid issues with CWD
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'praisa_demo.db')}"

# Create SQLAlchemy engine
# check_same_thread=False is required for SQLite to work with FastAPI
# (FastAPI uses multiple threads for async operations)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # SQLite-specific setting
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


def search_patients(
    name: str = None,
    abha: str = None,
    aadhaar: str = None,
    phone: str = None,
    hospital_id: str = None,
):
    """
    Search patients by name, ABHA (exact), Aadhaar (exact), or phone (exact).
    """
    print(
        f"[DEBUG] search_patients called with: name={name}, abha={abha}, "
        f"aadhaar={aadhaar}, phone={phone}, hosp={hospital_id}"
    )
    with get_db() as db:
        results = []

        # Priority 1: ABHA (Government ID) - Exact Match
        if abha:
            # Clean input
            clean_abha = abha.replace("-", "").replace(" ", "").strip()

            # OPTIMIZATION: Try exact match first (Uses Index = Fast)
            sql_fast = "SELECT * FROM patients WHERE abha_number = :val"
            params = {"val": clean_abha}  # Try cleaned version first

            if hospital_id:
                sql_fast += " AND hospital_id = :hosp"
                params["hosp"] = hospital_id

            query_fast = text(sql_fast)
            results = db.execute(query_fast, params).mappings().all()

            # If no results, try formatted search (or if input had dashes)
            # This handles cases where DB has dashes "12-34" but user searched "1234"
            if not results:
                # Fallback to REPLACEd query (Full Scan)
                sql = (
                    "SELECT * FROM patients WHERE "
                    "REPLACE(REPLACE(abha_number, '-', ''), ' ', '') = :val"
                )
                if hospital_id:
                    sql += " AND hospital_id = :hosp"
                results = db.execute(text(sql), params).mappings().all()

        # Priority 2: Aadhaar (Government ID) - Exact Match
        elif aadhaar:
            # Clean input
            clean_aadhaar = aadhaar.replace("-", "").replace(" ", "").strip()

            # OPTIMIZATION: Try exact match first (Uses Index = Fast)
            sql_fast = "SELECT * FROM patients WHERE aadhaar_number = :val"
            params = {"val": clean_aadhaar}

            if hospital_id:
                sql_fast += " AND hospital_id = :hosp"
                params["hosp"] = hospital_id

            results = db.execute(text(sql_fast), params).mappings().all()

            if not results:
                # Fallback (though Aadhaar is usually clean)
                sql = (
                    "SELECT * FROM patients WHERE "
                    "REPLACE(REPLACE(aadhaar_number, '-', ''), ' ', '') = :val"
                )
                if hospital_id:
                    sql += " AND hospital_id = :hosp"
                results = db.execute(text(sql), params).mappings().all()

        # Priority 3: Phone - Exact Match
        elif phone:
            # Clean the search phone (remove common prefixes and separators)
            clean_phone = (
                phone.replace("+91", "").replace("-", "").replace(" ", "").strip()
            )
            # Try last 10 digits as exact match
            last_10 = clean_phone[-10:] if len(clean_phone) >= 10 else clean_phone

            # OPTIMIZATION: Try exact match first
            sql_fast = "SELECT * FROM patients WHERE mobile = :val"
            params = {"val": last_10}

            if hospital_id:
                sql_fast += " AND hospital_id = :hosp"
                params["hosp"] = hospital_id

            results = db.execute(text(sql_fast), params).mappings().all()

            if not results:
                # Fallback to flexible search
                # Phone search: Flexible match on last 10 digits (PRIORITY 2)
                sql = """
                    SELECT * FROM patients
                    WHERE SUBSTR(
                        REPLACE(REPLACE(REPLACE(mobile, '+91', ''), '-', ''), ' ', ''),
                        -10
                    ) = :p_phone
                """
                params = {"p_phone": last_10}
                if hospital_id:
                    sql += " AND hospital_id = :hosp"
                    params["hosp"] = hospital_id
                results = db.execute(text(sql), params).mappings().all()

        elif name:
            # 1. Exact/Partial Match (Standard SQL)
            sql = "SELECT * FROM patients WHERE lower(name) LIKE :name"
            params = {"name": f"%{name.lower()}%"}

            if hospital_id:
                sql += " AND hospital_id = :hosp"
                params["hosp"] = hospital_id

            query = text(sql + " LIMIT 20")
            sql_results = [
                dict(row) for row in db.execute(query, params).mappings().all()
            ]

            # 2. Fuzzy Match (Typo Resilience)
            # If we don't have enough exact matches, find candidates using fuzzy similarity
            if len(sql_results) < 5:
                # Fetch all patients (or filtered by hospital)
                all_sql = "SELECT * FROM patients"
                all_params = {}
                if hospital_id:
                    all_sql += " WHERE hospital_id = :hosp"
                    all_params["hosp"] = hospital_id

                all_query = text(all_sql)
                all_patients = [
                    dict(row)
                    for row in db.execute(all_query, all_params).mappings().all()
                ]

                # Extract names for comparison
                names_map = {p["id"]: p["name"] for p in all_patients}

                # Find top fuzzy matches
                fuzzy_results = process.extract(
                    name,
                    names_map.values(),
                    scorer=fuzz.ratio,
                    limit=10,
                    score_cutoff=70,
                )

                # Deduplicate and merge
                matched_names = [res[0] for res in fuzzy_results]
                for p in all_patients:
                    if p["name"] in matched_names and p not in sql_results:
                        sql_results.append(p)

            results = sql_results[:10]  # Return top 10

        else:
            # No search criteria provided
            return []

        # Convert all results to regular mutable dicts to allow adding fields later
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
        query = text(
            """
            SELECT * FROM visits
            WHERE patient_id = :pid
            ORDER BY admission_date DESC
        """
        )

        # Execute and convert results
        results = db.execute(query, {"pid": patient_id}).mappings().all()
        return [dict(row) for row in results]
