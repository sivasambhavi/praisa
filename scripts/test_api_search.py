"""Test API search functionality"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("API SEARCH FUNCTIONALITY TEST")
print("=" * 70)

# Test 1: Search by name (no hospital filter)
print("\n1. SEARCH BY NAME (no hospital filter):")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/api/patients/search", params={"name": "Ramesh"})
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {data['count']} patients")
        for p in data['results'][:5]:
            print(f"  - {p['patient_id']} | {p['name']} | {p['hospital_id']}")
    else:
        print(f"✗ Error {response.status_code}: {response.text}")
except Exception as e:
    print(f"✗ Request failed: {e}")

# Test 2: Search with hospital_a filter
print("\n2. SEARCH BY NAME + HOSPITAL FILTER (hospital_a):")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/api/patients/search", params={
        "name": "Ramesh",
        "hospital_id": "hospital_a"
    })
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {data['count']} patients in hospital_a")
        for p in data['results']:
            print(f"  - {p['patient_id']} | {p['name']} | {p['hospital_id']}")
    else:
        print(f"✗ Error {response.status_code}: {response.text}")
except Exception as e:
    print(f"✗ Request failed: {e}")

# Test 3: Search all 5 hospitals
print("\n3. SEARCH ACROSS ALL 5 HOSPITALS:")
print("-" * 70)
for hosp in ['hospital_a', 'hospital_b', 'hospital_c', 'hospital_d', 'hospital_e']:
    try:
        response = requests.get(f"{BASE_URL}/api/patients/search", params={
            "name": "a",  # Very broad search
            "hospital_id": hosp
        })
        if response.status_code == 200:
            data = response.json()
            print(f"✓ {hosp}: {data['count']} results")
        else:
            print(f"✗ {hosp}: Error {response.status_code}")
    except Exception as e:
        print(f"✗ {hosp}: {e}")

# Test 4: Get specific patient
print("\n4. GET SPECIFIC PATIENT (HA001):")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/api/patients/HA001")
    if response.status_code == 200:
        p = response.json()
        print(f"✓ Found patient:")
        print(f"  ID: {p['patient_id']}")
        print(f"  Name: {p['name']}")
        print(f"  Hospital: {p['hospital_id']}")
        print(f"  ABHA: {p.get('abha_number', 'N/A')}")
    else:
        print(f"✗ Error {response.status_code}: {response.text}")
except Exception as e:
    print(f"✗ Request failed: {e}")

print("\n" + "=" * 70)
print("END OF TEST")
print("=" * 70)
