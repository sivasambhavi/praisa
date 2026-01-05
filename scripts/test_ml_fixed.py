"""Test FIXED ML matcher with Rohit vs Ramehs"""
import sys
sys.path.append('.')

# Force reload to get new changes
import importlib
from app.matching import ml_matcher
importlib.reload(ml_matcher)
from app.matching.ml_matcher import MLPatientMatcher

# Initialize matcher (will load new weights)
matcher = MLPatientMatcher()

# Patient A: HD009 - Rohit Malhotra
patient_a = {
    "patient_id": "HD009",
    "hospital_id": "hospital_d",
    "name": "Rohit Malhotra",
    "dob": "1990-08-28",
    "mobile": "6797723352",
    "gender": "F",
    "abha_number": "554919",
    "address": "545 Street 15",
    "state": "Bihar"
}

# Patient B: HA013 - Ramehs Malhotra
patient_b = {
    "patient_id": "HA013",
    "hospital_id": "hospital_a",
    "name": "Ramehs Malhotra",
    "dob": "1984-02-03",
    "mobile": "7470384348",
    "gender": "M",
    "abha_number": "86529394595101",
    "address": "House No 36 Street 13",
    "state": "Bihar"
}

print("=" * 70)
print("TESTING FIXED ML MATCHER")
print("=" * 70)

print(f"\nPatient A: {patient_a['name']} ({patient_a['patient_id']}) - Gender: {patient_a['gender']}")
print(f"Patient B: {patient_b['name']} ({patient_b['patient_id']}) - Gender: {patient_b['gender']}")

# Get detailed prediction
result = matcher.predict_detailed(patient_a, patient_b)

print("\n" + "=" * 70)
print("RESULT")
print("=" * 70)
print(f"Match Probability: {result['prob']:.4f} ({result['prob']*100:.2f}%)")
print(f"Method: {result['method']}")
print(f"Matched Fields: {result['matched_fields']}")

print("\n" + "=" * 70)
print("ANALYSIS")
print("=" * 70)
print(f"✗ First names: 'Rohit' vs 'Ramehs' - DIFFERENT")
print(f"✓ Last names: 'Malhotra' vs 'Malhotra' - SAME (but not enough!)")
print(f"✗ ABHA: {patient_a['abha_number']} vs {patient_b['abha_number']} - DIFFERENT")
print(f"✗ DOB: {patient_a['dob']} vs {patient_b['dob']} - DIFFERENT")
print(f"✗ Gender: {patient_a['gender']} vs {patient_b['gender']} - DIFFERENT")
print(f"✓ State: {patient_a['state']} vs {patient_b['state']} - SAME")

print("\n" + "=" * 70)
if result['prob'] < 0.6:
    print("✅ CORRECT: Low score indicates these are DIFFERENT people!")
    print(f"   Score {result['prob']*100:.2f}% is below 60% threshold → NO_MATCH")
else:
    print("❌ STILL WRONG: Score too high for different people!")
    print(f"   Score {result['prob']*100:.2f}% should be < 60%")
print("=" * 70)

# Also test a TRUE match (golden pair)
print("\n\n" + "=" * 70)
print("TESTING WITH TRUE MATCH (HA001 vs HB001)")
print("=" * 70)

golden_a = {
    "patient_id": "HA001",
    "name": "Ramesh Singh",
    "dob": "1985-03-15",
    "mobile": "9876543210",
    "gender": "M",
    "abha_number": "12-3456-7890-1234"
}

golden_b = {
    "patient_id": "HB001",
    "name": "Ramehs Singh",
    "dob": "1985-03-15",
    "mobile": "+91-9876543210",
    "gender": "M",
    "abha_number": "12-3456-7890-1234"
}

print(f"\nPatient A: {golden_a['name']} - ABHA: {golden_a['abha_number']}")
print(f"Patient B: {golden_b['name']} - ABHA: {golden_b['abha_number']}")

golden_result = matcher.predict_detailed(golden_a, golden_b)
print(f"\nMatch Score: {golden_result['prob']*100:.2f}%")
print(f"Method: {golden_result['method']}")

if golden_result['prob'] >= 0.8:
    print("✅ CORRECT: High score for true golden pair!")
else:
    print("❌ PROBLEM: Golden pair should score high!")
