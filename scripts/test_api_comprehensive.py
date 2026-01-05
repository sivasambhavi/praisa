"""Test API directly with Python requests"""
import requests
import json
import time

# Wait a moment for server
time.sleep(2)

print("=" * 70)
print("TESTING PRAISA API")
print("=" * 70)

BASE_URL = "http://localhost:8000"

# Test 1: Basic search
print("\n1. Search for 'ramesh' (no hospital filter):")
try:
    response = requests.get(f"{BASE_URL}/api/patients/search", params={"name": "ramesh"}, timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found: {data['count']} patients")
        for p in data['results'][:3]:
            print(f"     - {p['patient_id']}: {p['name']} ({p['hospital_id']})")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Exception: {e}")

# Test 2: Search with hospital filter
print("\n2. Search 'ramesh' in hospital_b:")
try:
    response = requests.get(f"{BASE_URL}/api/patients/search", params={"name": "ramesh", "hospital_id": "hospital_b"}, timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found: {data['count']} patients")
        for p in data['results']:
            print(f"     - {p['patient_id']}: {p['name']}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Exception: {e}")

# Test 3: Get specific patient
print("\n3. Get patient HA001:")
try:
    response = requests.get(f"{BASE_URL}/api/patients/HA001", timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        p = response.json()
        print(f"   Name: {p['name']}")
        print(f"   Hospital: {p['hospital_id']}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Exception: {e}")

# Test 4: Match two patients
print("\n4. Match HA001 with HB001:")
try:
    # Get both patients first
    p1 = requests.get(f"{BASE_URL}/api/patients/HA001", timeout=5).json()
    p2 = requests.get(f"{BASE_URL}/api/patients/HB001", timeout=5).json()
    
    # Match them
    response = requests.post(f"{BASE_URL}/api/match", json={
        "patient_a": p1,
        "patient_b": p2
    }, timeout=5)
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        match = response.json()
        print(f"   Score: {match['match_score']}")
        print(f"   Method: {match['method']}")
        print(f"   Recommendation: {match['recommendation']}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Exception: {e}")

print("\n" + "=" * 70)
