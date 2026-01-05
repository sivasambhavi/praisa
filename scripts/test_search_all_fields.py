
import requests
import time
import json

BASE_URL = "http://localhost:8000/api/patients/search"

def test_search(params, description):
    print(f"\n--- Testing {description} ---")
    print(f"Params: {params}")
    
    start_time = time.time()
    try:
        response = requests.get(BASE_URL, params=params)
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
                print(f"First Result: {first.get('name')} | {first.get('hospital_id')} | {first.get('aadhaar_number', 'N/A')}")
                return True
            else:
                print("No results found.")
                return False
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Exception: {e}")
        return False

def run_all_tests():
    print("Starting End-to-End Search Verification...")
    
    # 1. Name Search (Hospital Specific)
    test_search({"name": "Ramesh", "hospital_id": "hospital_a"}, "Name Search (Ramesh @ Hosp A)")
    
    # 2. ABHA Search (Existing) - Use a likely existing one or just test the query speed
    # We will use a known one from the CSV we saw earlier if possible, or just a dummy one to test 'No Match' speed
    test_search({"abha": "12-3456-7890-1234"}, "ABHA Search (Known Dummy)")
    
    # 3. Phone Search
    test_search({"phone": "9876543210"}, "Phone Search")
    
    # 4. Aadhaar Search (New) - We generated random ones, so getting a hit is hard without looking up DB.
    # But we can test the 'No Match' speed which exercises the same full table scan logic.
    test_search({"aadhaar": "123456789012"}, "Aadhaar Search (Random No Match)")
    
    # 5. Aadhaar Search (Valid Format Check)
    test_search({"aadhaar": "1111-2222-3333"}, "Aadhaar Search (Formatted Input)")

if __name__ == "__main__":
    run_all_tests()
