from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api_health():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_patient_details_success():
    """Test getting a patient by ID (Found)"""
    response = client.get("/api/patients/HA001")
    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == "HA001"
    assert "Ramesh" in data["name"]


def test_get_patient_details_not_found():
    """Test getting a patient by ID (Not Found)"""
    response = client.get("/api/patients/NONEXISTENT")
    assert response.status_code == 404
    assert response.json()["detail"] == "Patient NONEXISTENT not found"


def test_search_patients_by_name():
    """Test search by name parameter"""
    response = client.get("/api/patients/search?name=Ramesh")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] > 0
    names = [p["name"] for p in data["results"]]
    # Should check if any result contains Ramesh
    assert any("Ramesh" in name for name in names)


def test_search_patients_by_abha():
    """Test search by ABHA parameter"""
    response = client.get("/api/patients/search?abha=12-3456-7890-1234")
    assert response.status_code == 200
    data = response.json()
    # Should match only 1 ideally, or more if duplicates (but we handle logic)
    assert data["count"] >= 1
    assert data["results"][0]["patient_id"] == "HA001"


def test_search_patients_missing_params():
    """Test search without required parameters"""
    response = client.get("/api/patients/search")
    assert response.status_code == 400
    assert "Provide 'name', 'abha', 'aadhaar', or 'phone' query parameter" in response.json()["detail"]


def test_get_patient_history_success():
    """Test retrieving patient history"""
    response = client.get("/api/patients/HA001/history")
    assert response.status_code == 200
    data = response.json()
    assert "patient" in data
    assert "visits" in data
    assert data["patient"]["patient_id"] == "HA001"
    assert len(data["visits"]) > 0


def test_get_patient_history_not_found():
    """Test retrieving history for non-existent patient"""
    response = client.get("/api/patients/NONEXISTENT/history")
    assert response.status_code == 404
