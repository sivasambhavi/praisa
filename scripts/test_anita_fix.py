"""Test ML matcher with Anita Desai vs Anita Verma AFTER FIX"""
import sys
sys.path.append('.')

import importlib
from app.matching import ml_matcher
importlib.reload(ml_matcher)
from app.matching.ml_matcher import MLPatientMatcher

matcher = MLPatientMatcher()

# Anita Desai
patient_a = {
    "patient_id": "HA008",
    "name": "Anita Desai",
   "dob": "1992-12-10",
    "mobile": "9789012345",
    "gender": "F",
    "abha_number": "12-3456-7890-8901"
}

# Anita Verma
patient_b = {
    "patient_id": "HD013",
    "name": "Anita Verma",
    "dob": "1975-08-21",
    "mobile": "6655274606",
    "gender": "M",
    "abha_number": "63754344673669"
}

print("=" * 70)
print("TESTING FIXED ML MATCHER - Anita Desai vs Anita Verma")
print("=" * 70)

print(f"\nPatient A: {patient_a['name']} ({patient_a['patient_id']})")
print(f"  ABHA: {patient_a['abha_number']}, DOB: {patient_a['dob']}, Gender: {patient_a['gender']}")

print(f"\nPatient B: {patient_b['name']} ({patient_b['patient_id']})")
print(f"  ABHA: {patient_b['abha_number']}, DOB: {patient_b['dob']}, Gender: {patient_b['gender']}")

result = matcher.predict_detailed(patient_a, patient_b)

print("\n" + "=" * 70)
print("RESULT")
print("=" * 70)
print(f"Match Score: {result['prob']*100:.2f}%")
print(f"Method: {result['method']}")

print("\n" + "=" * 70)
print("COMPARISON")
print("=" * 70)
print(f"✓ First Name: Anita vs Anita - SAME")
print(f"✗ Last Name: Desai vs Verma - DIFFERENT!")
print(f"✗ ABHA: {patient_a['abha_number']} vs {patient_b['abha_number']} - DIFFERENT!")
print(f"✗ DOB: {patient_a['dob']} vs {patient_b['dob']} - DIFFERENT!")
print(f"✗ Gender: {patient_a['gender']} vs {patient_b['gender']} - DIFFERENT!")

print("\n" + "=" * 70)
if result['prob'] < 0.5:
    print(f"✅ CORRECT! Score {result['prob']*100:.2f}% is below 50% → NO_MATCH")
    print("   Different last names + no ABHA/DOB match = Different people!")
else:
    print(f"❌ STILL WRONG! Score {result['prob']*100:.2f}% should be < 50%")
print("=" * 70)
