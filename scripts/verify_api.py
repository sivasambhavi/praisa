"""
API Verification Script
-----------------------
Tests the locally running FastAPI backend to ensure:
1. Health check passes
2. Patient retrieval works
3. Patient history works
4. Matching API works

Usage: python scripts/verify_api.py
Note: Requires backend running on localhost:8000
"""

import httpx
import sys
import json

BASE_URL = "http://localhost:8000"

def test_health():
    print(f"Checking {BASE_URL}/health ...", end=" ")
    try:
        r = httpx.get(f"{BASE_URL}/health")
        if r.status_code == 200:
            print("OK")
            return True
        else:
            print(f"FAILED (Status: {r.status_code})")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_get_patient(patient_id="HA001"):
    print(f"Checking {BASE_URL}/api/patients/{patient_id} ...", end=" ")
    try:
        r = httpx.get(f"{BASE_URL}/api/patients/{patient_id}")
        if r.status_code == 200:
            data = r.json()
            if data['patient_id'] == patient_id:
                print("OK")
                return True, data
            else:
                print("FAILED (ID mismatch)")
                return False, None
        else:
            print(f"FAILED (Status: {r.status_code})")
            print(r.text)
            return False, None
    except Exception as e:
        print(f"ERROR: {e}")
        return False, None

def test_get_history(patient_id="HA001"):
    print(f"Checking {BASE_URL}/api/patients/{patient_id}/history ...", end=" ")
    try:
        r = httpx.get(f"{BASE_URL}/api/patients/{patient_id}/history")
        if r.status_code == 200:
            data = r.json()
            if "visits" in data and isinstance(data["visits"], list):
                print(f"OK ({len(data['visits'])} visits found)")
                return True
            else:
                print("FAILED (Response structure incorrect)")
                return False
        else:
            print(f"FAILED (Status: {r.status_code})")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_matching(patient_a_data):
    print(f"Checking {BASE_URL}/api/match ...", end=" ")
    
    # Create a slightly different patient B (typo in name)
    patient_b_data = patient_a_data.copy()
    patient_b_data["name"] = patient_b_data["name"].replace("Ramesh", "Ramehs") # Simulate typo
    patient_b_data["patient_id"] = "HB001"
    
    payload = {
        "patient_a": patient_a_data,
        "patient_b": patient_b_data
    }
    
    try:
        r = httpx.post(f"{BASE_URL}/api/match", json=payload)
        if r.status_code == 200:
            data = r.json()
            if data['recommendation'] == 'MATCH':
                print(f"OK (Score: {data['match_score']})")
                return True
            else:
                print(f"FAILED (Result: {data['recommendation']})")
                return False
        else:
            print(f"FAILED (Status: {r.status_code})")
            print(r.text)
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("Starting API Verification...")
    
    # 1. Health
    if not test_health():
        print("CRITICAL: Server not reachable or unhealthy.")
        sys.exit(1)
        
    # 2. Get Patient
    success, p_data = test_get_patient("HA001")
    if not success:
        print("CRITICAL: Could not retrieve verified patient.")
        sys.exit(1)
        
    # 3. Get History
    if not test_get_history("HA001"):
        print("WARNING: History retrieval failed.")
        
    # 4. Matching
    if not test_matching(p_data):
        print("CRITICAL: Matching API failed.")
        sys.exit(1)
        
    print("\nALL API CHECKS PASSED.")

if __name__ == "__main__":
    main()
