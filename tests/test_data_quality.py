"""
Test Data Quality and Resilience

Verifies that the database contains the expected diverse data scenarios
and that the system handles them correctly.
"""

from datetime import datetime
from sqlalchemy import text
from app.database.db import get_db, get_patient, search_patients


def test_five_hospitals_present():
    """Verify that data from at least 5 different hospitals exists."""
    with get_db() as db:
        # Use text() for raw SQL queries with SQLAlchemy
        query = text("SELECT DISTINCT hospital_id FROM patients")
        result = db.execute(query)
        hospitals = [row[0] for row in result.fetchall()]

    assert len(hospitals) >= 5
    assert "hospital_a" in hospitals
    assert "hospital_e" in hospitals


def test_invalid_mobile_numbers_exist():
    """Verify that we have patients with invalid mobile numbers (short or starting with 0)."""
    with get_db() as db:
        # Check for short numbers
        query_short = text("SELECT count(*) FROM patients WHERE length(mobile) < 10")
        short_count = db.execute(query_short).scalar()

        # Check for numbers starting with 0
        query_zero = text("SELECT count(*) FROM patients WHERE mobile LIKE '0%'")
        zero_start_count = db.execute(query_zero).scalar()

    # We expect some bad data based on our generation script
    assert short_count > 0 or zero_start_count > 0


def test_can_retrieve_patient_with_bad_mobile():
    """Ensure system doesn't crash when retrieving a patient with bad mobile number."""
    with get_db() as db:
        query = text(
            "SELECT patient_id FROM patients WHERE length(mobile) < 10 LIMIT 1"
        )
        row = db.execute(query).first()

    if row:
        patient_id = row[0]
        # Use correct function name get_patient
        patient = get_patient(patient_id)
        assert patient is not None
        assert len(patient["mobile"]) < 10


def test_extreme_dates_exist():
    """Verify presence of extreme dates (very old or future)."""
    with get_db() as db:
        query = text("SELECT dob FROM patients")
        result = db.execute(query)
        dobs = [row[0] for row in result.fetchall()]

    extreme_found = False
    current_year = datetime.now().year

    for dob_str in dobs:
        try:
            dob_year = int(dob_str.split("-")[0])
            # Check for very old (>100 years) or future
            if dob_year < (current_year - 100) or dob_year > current_year:
                extreme_found = True
                break
        except Exception:
            continue

    assert extreme_found


def test_typo_matching_resilience():
    """Verify that matching works even with the introduced typos."""
    # We generated "Ramehs" instead of "Ramesh" in some cases.
    # Let's try to match "Ramesh Singh" against the DB.
    # It should find the "Ramehs Singh" records via fuzzy/phonetic search.

    # We generated "Ramehs" instead of "Ramesh" in some cases.
    # First, let's find a "Ramehs" in the DB to test against.
    with get_db() as db:
        query = text("SELECT * FROM patients WHERE name LIKE '%mehs%' LIMIT 1")
        row = db.execute(query).mappings().first()

    if row:
        db_patient = dict(row)
        # Search query details (User inputting "Ramesh")
        search_query = {
            "name": "Ramesh Singh",
            "gender": db_patient.get("gender"),
            "mobile": db_patient.get("mobile"),
            "dob": db_patient.get("dob"),
        }

        # Import the correct function
        from app.matching.simple_matcher import match_patients

        # Match "Ramesh" (search) against "Ramehs" (db record)
        result = match_patients(search_query, db_patient)

        # Verify result contains high score even with typo
        assert result["match_score"] >= 80
        assert result["recommendation"] == "MATCH"
        print(
            f"Successfully matched 'Ramesh' to '{db_patient['name']}' "
            f"with score {result['match_score']}"
        )


def test_invalid_abha_handling():
    """Ensure invalid ABHA numbers (wrong length) don't break search."""
    # Find a patient with invalid ABHA
    with get_db() as db:
        query = text(
            "SELECT abha_number FROM patients WHERE length(abha_number) != 14 LIMIT 1"
        )
        row = db.execute(query).first()

    if row:
        invalid_abha = row[0]
        # Searching by this invalid ABHA should still work (exact match)
        # or at least not crash.
        results = search_patients(abha=invalid_abha)
        assert len(results) > 0
        assert results[0]["abha_number"] == invalid_abha
