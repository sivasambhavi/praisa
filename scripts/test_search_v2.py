
import requests
import time
import sys

# Use 127.0.0.1 to avoid IPv6 lookup delays on Windows
BASE_URL = "http://127.0.0.1:8000/api/patients/search"

def test_search(params, description):
    print(f"\n--- Testing {description} ---")
    print(f"Params: {params}")
    sys.stdout.flush()
    
    start_time = time.time()
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        end_time = time.time()
        
        duration_ms = (end_time - start_time) * 1000
        print(f"Status: {response.status_code}")
        print(f"Time: {duration_ms:.2f} ms")
        
        if response.status_code == 200:
            data = response.json()
            count = data.get("count", 0)
            search_type = data.get("search_type", "unknown")
            print(f"Results: {count}")
            print(f"Search Type: {search_type}")
            
            if count > 0:
                first = data["results"][0]
                print(f"First Result: {first.get('name')} | Aadhaar: {first.get('aadhaar_number', 'N/A')}")
            else:
                print("No results found.")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")
    sys.stdout.flush()

if __name__ == "__main__":
    print("Starting End-to-End Search Verification (v2)...")
    # Quick connectivity check
    try:
        requests.get("http://127.0.0.1:8000/docs", timeout=2)
        print("Backend is reachable.")
    except:
        print("Backend seems down!")
        sys.exit(1)

    # 1. Name
    test_search({"name": "Dinesh", "hospital_id": "hospital_a"}, "Name Search")
    
    # 2. Aadhaar (From Dinesh Shah)
    test_search({"aadhaar": "274893044202"}, "Aadhaar Search")
    
    # 3. Phone (From Dinesh Shah)
    test_search({"phone": "8524167277"}, "Phone Search")
