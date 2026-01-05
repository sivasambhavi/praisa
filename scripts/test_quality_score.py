
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import db
from app.utils.quality_scorer import calculate_data_quality

def test_data_quality():
    print("Testing Data Quality Scorer...")
    
    # Get a patient
    patients = db.search_patients(name="Ramesh")
    if not patients:
        print("No patients found to test.")
        return

    patient = patients[0]
    print(f"Testing patient: {patient['name']} ({patient['patient_id']})")
    
    # Calculate score
    score, missing = calculate_data_quality(patient)
    
    print(f"Quality Score: {score}/100")
    print(f"Missing Fields: {missing}")
    
    if score > 0:
        print("✅ Data Quality Scorer Test Passed")
    else:
        print("❌ Data Quality Scorer Test Failed (Score is 0)")

if __name__ == "__main__":
    test_data_quality()
