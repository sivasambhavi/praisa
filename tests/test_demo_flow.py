"""
Automated Integration Test for PRAISA Demo Flow
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_demo_golden_path():
    print("\n--- Starting Automated Demo Flow ---")

    # Step 1: Search for "Ramesh"
    print("1. Searching for 'Ramesh'...")
    response = client.get("/api/patients/search?name=Ramesh")
    assert response.status_code == 200
    results = response.json()["results"]

    # Verify HA001 is found
    ha_patient = next((p for p in results if p["patient_id"] == "HA001"), None)
    assert ha_patient is not None, "Ramesh (HA001) not found in search results"
    print(f"   found: {ha_patient['name']} (ID: {ha_patient['patient_id']})")

    # Step 2: Match with Hospital B (HB001)
    # In the demo, we assume the user selects HB001 manually or via UI logic
    print("2. Matching HA001 with HB001...")

    # We first need HB001 details to send in the match request
    # (The frontend fetches this, so we simulate that here)
    hb_response = client.get("/api/patients/HB001")
    assert hb_response.status_code == 200
    hb_patient = hb_response.json()

    # Perform Match
    match_payload = {"patient_a": ha_patient, "patient_b": hb_patient}
    match_response = client.post("/api/match", json=match_payload)
    assert match_response.status_code == 200
    match_result = match_response.json()

    # Verify Match Score
    print(f"   Match Score: {match_result['match_score']}%")
    print(f"   Method: {match_result['method']}")
    assert match_result["match_score"] >= 90.0, "Match score too low"
    assert match_result["recommendation"] == "MATCH", "Recommendation should be MATCH"

    # Step 3: Fetch Unified History
    print("3. Fetching History for both patients...")

    # History A
    hist_a = client.get(f"/api/patients/{ha_patient['patient_id']}/history")
    assert hist_a.status_code == 200
    visits_a = hist_a.json()["visits"]
    print(f"   Hospital A Visits: {len(visits_a)}")

    # History B
    hist_b = client.get(f"/api/patients/{hb_patient['patient_id']}/history")
    assert hist_b.status_code == 200
    visits_b = hist_b.json()["visits"]
    print(f"   Hospital B Visits: {len(visits_b)}")

    # Verify we have data to combine
    assert len(visits_a) > 0, "No visits found for Hospital A"
    assert len(visits_b) > 0, "No visits found for Hospital B"

    print("\n--- Demo Flow Verified Successfully! ---")
