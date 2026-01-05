
import requests
import time
import sys
import json

BASE_URL = "http://localhost:8000"

def wait_for_server():
    print("Waiting for server to start...")
    for _ in range(30):
        try:
            resp = requests.get(f"{BASE_URL}/health")
            if resp.status_code == 200:
                print("✅ Server is UP!")
                return True
        except:
            pass
        time.sleep(1)
    print("❌ Server failed to start.")
    return False

def test_search_name():
    print("\n--- Testing Search by Name (Ramesh) ---")
    resp = requests.get(f"{BASE_URL}/api/patients/search", params={"name": "Ramesh"})
    if resp.status_code == 200:
        data = resp.json()
        count = data["count"]
        print(f"✅ Search successful. Found {count} results.")
        
        # Verify Quality Score
        if count > 0:
            first = data["results"][0]
            qs = first.get("quality_score")
            print(f"Patient: {first['name']}, Quality Score: {qs}/100")
            if qs is not None:
                print("✅ Quality Score present in response.")
            else:
                print("❌ Quality Score MISSING.")
            return first
    else:
        print(f"❌ Search failed: {resp.status_code} - {resp.text}")
    return None

def test_history(patient_id):
    print(f"\n--- Testing History for {patient_id} ---")
    resp = requests.get(f"{BASE_URL}/api/patients/{patient_id}/history")
    if resp.status_code == 200:
        data = resp.json()
        visits = data["visits"]
        print(f"✅ History fetch successful. Found {len(visits)} visits.")
        return True
    else:
        print(f"❌ History fetch failed: {resp.status_code}")
        return False

def test_match(p1, p2):
    print(f"\n--- Testing Match between {p1['name']} and {p2['name']} ---")
    payload = {
        "patient_a": p1,
        "patient_b": p2
    }
    resp = requests.post(f"{BASE_URL}/api/match", json=payload)
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ Match successful.")
        print(f"Score: {data['match_score']}")
        print(f"Confidence: {data['confidence']}")
        print(f"Method: {data['method']}")
        return True
    else:
        print(f"❌ Match failed: {resp.status_code} - {resp.text}")
        return False

def run_tests():
    if not wait_for_server():
        sys.exit(1)

    # 1. Search
    p1 = test_search_name()
    if not p1:
        print("Stopping tests due to search failure.")
        return

    # 2. History
    test_history(p1["patient_id"])

    # 3. Match (Need a second patient)
    # Let's search for "Ramehs" to find a match target
    print("\nSearching for match target 'Ramehs'...")
    resp = requests.get(f"{BASE_URL}/api/patients/search", params={"name": "Ramehs"})
    if resp.status_code == 200 and resp.json()["count"] > 0:
        p2 = resp.json()["results"][0]
        test_match(p1, p2)
    else:
        print("Could not find 'Ramehs' to test matching.")

if __name__ == "__main__":
    run_tests()
