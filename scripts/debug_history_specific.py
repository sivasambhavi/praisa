
import requests
import json

BASE_URL = "http://localhost:8000/api/patients"

def check_history(pid):
    try:
        url = f"{BASE_URL}/{pid}/history"
        print(f"Fetching history for {pid}...")
        resp = requests.get(url)
        data = resp.json()
        
        visits = data.get("visits", [])
        print(f"Visits found: {len(visits)}")
        print(json.dumps(visits, indent=2))
        
        return len(visits)
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0

if __name__ == "__main__":
    count_a = check_history("HA001") # Ramesh (Hospital A)
    count_b = check_history("HB001") # Ramehs (Hospital B - Linked)

    if count_a == 0 and count_b == 0:
        print("\n❌ MAJOR ISSUE: No visits for Demo Persona (Ramesh). Unified History will be blank!")
    else:
        print("\n✅ Visits found. History should work.")
