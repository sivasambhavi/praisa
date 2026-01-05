"""Simple test of backend API"""
import requests

try:
    print("Testing backend at http://localhost:8000/api/patients/search?name=ramesh")
    response = requests.get("http://localhost:8000/api/patients/search", params={"name": "ramesh"}, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
