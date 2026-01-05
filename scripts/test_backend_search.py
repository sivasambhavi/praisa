"""Test backend phone search directly"""
import requests

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("TESTING BACKEND PHONE SEARCH")
print("=" * 70)

# Test 1: Phone search
phone = "9874214071"
print(f"\n1. Searching for phone: {phone}")
try:
    response = requests.get(f"{BASE_URL}/api/patients/search", params={"phone": phone}, timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found: {data['count']} patients")
        print(f"   Search type: {data.get('search_type', 'unknown')}")
        for p in data['results']:
            print(f"     - {p['patient_id']}: {p['name']} | Mobile: {p.get('mobile', 'N/A')}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Exception: {e}")

# Test 2: Name search for Ramesh
print(f"\n2. Searching for name: Ramesh")
try:
    response = requests.get(f"{BASE_URL}/api/patients/search", params={"name": "ramesh"}, timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found: {data['count']} patients")
        for p in data['results'][:3]:
            print(f"     - {p['patient_id']}: {p['name']} | {p.get('hospital_id', 'N/A')}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Exception: {e}")

# Test 3: ABHA search
print(f"\n3. Searching for ABHA: 12-3456-7890-1234")
try:
    response = requests.get(f"{BASE_URL}/api/patients/search", params={"abha": "12-3456-7890-1234"}, timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found: {data['count']} patients (cross-hospital)")
        print(f"   Search type: {data.get('search_type', 'unknown')}")
        for p in data['results']:
            print(f"     - {p['patient_id']}: {p['name']} | {p.get('hospital_id', 'N/A')}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Exception: {e}")

print("\n" + "=" * 70)
