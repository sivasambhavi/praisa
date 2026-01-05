"""Test ML matcher with Rohit vs Ramehs"""
import sys
sys.path.append('.')

from app.matching.ml_matcher import MLPatientMatcher

# Initialize matcher
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
print("ML MATCHER DETAILED ANALYSIS")
print("=" * 70)

print(f"\nPatient A: {patient_a['name']} ({patient_a['patient_id']})")
print(f"Patient B: {patient_b['name']} ({patient_b['patient_id']})")

# Get detailed prediction
result = matcher.predict_detailed(patient_a, patient_b)

print("\n" + "=" * 70)
print("ML PREDICTION RESULT")
print("=" * 70)
print(f"Probability: {result['prob']:.4f} ({result['prob']*100:.2f}%)")
print(f"Method: {result['method']}")
print(f"Matched Fields: {result['matched_fields']}")

print("\n" + "=" * 70)
print("FEATURE EXTRACTION")
print("=" * 70)
features = result['features']
for fname, fval in features.items():
    print(f"  {fname:25} = {fval:6.2f}")

print("\n" + "=" * 70)
print("WEIGHTED CONTRIBUTIONS")
print("=" * 70)
weights = matcher.weights
for fname in features:
    contribution = features[fname] * weights[fname]
    print(f"  {fname:25} = {features[fname]:6.2f} * {weights[fname]:5.2f} = {contribution:6.2f}")

print("\n" + "=" * 70)
print("ANALYSIS")
print("=" * 70)
print(f"\nFirst names: 'Rohit' vs 'Ramehs' - COMPLETELY DIFFERENT")
print(f"Last names: 'Malhotra' vs 'Malhotra' - SAME")
print(f"ABHA: {patient_a['abha_number']} vs {patient_b['abha_number']} - DIFFERENT")
print(f"DOB: {patient_a['dob']} vs {patient_b['dob']} - DIFFERENT")
print(f"State: {patient_a['state']} vs {patient_b['state']} - SAME (Bihar)")
print(f"\nPROBLEM: ML is over-weighting last name match + state match!")
print(f"Result: {result['prob']*100:.2f}% match is WRONG - should be <50%")
