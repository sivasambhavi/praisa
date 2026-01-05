"""Direct API test for ramehs search"""
import requests

BASE_URL = "http://localhost:8000"

print("Testing search for 'ramehs' in hospital_b...")
print("=" * 60)

try:
    response = requests.get(
        f"{BASE_URL}/api/patients/search",
        params={"name": "ramehs", "hospital_id": "hospital_b"},
        timeout=5
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ Success! Found {data['count']} patients")
        for p in data['results']:
            print(f"  - {p['patient_id']}: {p['name']}")
    else:
        print(f"\n✗ Error {response.status_code}")
        
except Exception as e:
    print(f"\n✗ Exception: {e}")
    import traceback
    traceback.print_exc()
