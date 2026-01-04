from app.database import db

# Assumes database is already populated by loader
# Ideally we should use a separate test DB, but for this demo we'll use the main one
# or mock the session. Given the requirements, testing against the populated DB is fine.


def test_get_patient_found():
    """Test getting an existing patient"""
    patient = db.get_patient("HA001")
    assert patient is not None
    assert patient["patient_id"] == "HA001"
    assert "Ramesh Singh" in patient["name"]


def test_get_patient_not_found():
    """Test getting a non-existent patient"""
    patient = db.get_patient("NONEXISTENT")
    assert patient is None


def test_search_patients_by_name():
    """Test searching patients by partial name"""
    results = db.search_patients(name="Ramesh")
    assert len(results) >= 1
    # Check if HA001 is in results
    patient_ids = [p["patient_id"] for p in results]
    assert "HA001" in patient_ids


def test_search_patients_by_name_case_insensitive():
    """Test case-insensitive search"""
    results = db.search_patients(name="ramesh")
    assert len(results) >= 1
    patient_ids = [p["patient_id"] for p in results]
    assert "HA001" in patient_ids


def test_search_patients_by_abha():
    """Test searching by exact ABHA number"""
    # HA001's ABHA: 12-3456-7890-1234
    results = db.search_patients(abha="12-3456-7890-1234")
    assert len(results) >= 1
    assert results[0]["patient_id"] == "HA001"


def test_search_patients_no_results():
    """Test search with no matches"""
    results = db.search_patients(name="XyZ123NotReal")
    assert len(results) == 0


def test_search_patients_empty_params():
    """Test search with no parameters (should return empty list based on implementation)"""
    results = db.search_patients()
    assert results == []


def test_get_patient_visits_found():
    """Test getting visits for a patient"""
    visits = db.get_patient_visits("HA001")
    assert len(visits) > 0
    assert visits[0]["patient_id"] == "HA001"


def test_get_patient_visits_no_visits():
    """Test getting visits for a patient with no visits (or non-existent patient)"""
    # Using a non-existent patient ID should return empty list
    visits = db.get_patient_visits("NONEXISTENT")
    assert len(visits) == 0
