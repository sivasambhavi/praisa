
import requests
import sys

BASE_URL = "http://localhost:8000/api/patients/search"

def test_search(type, value, hospital=None, expected_count=1):
    print(f"Testing {type} search: '{value}' ...")
    params = {}
    if type == "abha":
        params = {"abha": value}
    elif type == "phone":
        params = {"phone": value}
    elif type == "name":
        params = {"name": value}
        if hospital:
            params["hospital_id"] = hospital
            
    try:
        resp = requests.get(BASE_URL, params=params)
        data = resp.json()
        count = data.get("count", 0)
        
        if count >= expected_count:
            print(f"✅ Success! Found {count} results.")
            for p in data["results"][:1]:
                print(f"   Match: {p['name']} ({p.get('hospital_id')}) - ID: {p.get('patient_id')}")
        else:
            print(f"❌ Failed. Found {count} results, expected >= {expected_count}")
            print(f"   Response: {data}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        try:
            print(f"Status: {resp.status_code}")
            print(f"Body: {resp.text[:500]}")
        except:
            pass

if __name__ == "__main__":
    # 1. Test existing ABHA with dashes (from CSV line 2)
    test_search("abha", "12-3456-7890-1234")

    # 2. Test ABHA without dashes (simulating user input variation)
    test_search("abha", "12345678901234")

    # 3. Test Phone (from CSV line 2)
    test_search("phone", "9876543210")
    
    # 4. Test Phone with +91 (from CSV line 12)
    test_search("phone", "+91-9876543210")
