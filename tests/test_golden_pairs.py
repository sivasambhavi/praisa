"""
Test script for matching algorithms with golden pairs
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.db import get_patient
from app.matching.simple_matcher import match_patients

# Golden pairs from the database
golden_pairs = [
    ("HA001", "HB001", "Ramesh Singh", "Ramehs Singh"),
    ("HA002", "HB002", "Priya Sharma", "Prya Sharma"),
    ("HA003", "HB003", "Vijay Kumar", "Wijay Kumar"),
    ("HA004", "HB004", "Amit Kumar", "Amit Kumarr"),
    ("HA005", "HB005", "Sunita Gupta", "Suneeta Gupta"),
]

print("=" * 80)
print("PRAISA - Testing Matching Algorithms with Golden Pairs")
print("=" * 80)
print()

for ha_id, hb_id, name_a, name_b in golden_pairs:
    # Get patients from database
    patient_a = get_patient(ha_id)
    patient_b = get_patient(hb_id)

    if not patient_a or not patient_b:
        print(f"❌ {ha_id} or {hb_id} not found in database")
        continue

    # Match patients
    result = match_patients(patient_a, patient_b)

    # Display result
    score = result["match_score"]
    method = result["method"]
    recommendation = result["recommendation"]

    # Status indicators (ASCII for Windows compatibility)
    if score >= 90:
        status = "[OK]"
    elif score >= 80:
        status = "[!!]"
    else:
        status = "[XX]"

    print(f"{status} {ha_id} ({name_a:20s}) <-> {hb_id} ({name_b:20s})")
    print(f"   Score: {score:5.1f}% | Method: {method:20s} | {recommendation}")
    print()

print("=" * 80)
print("Test Complete!")
print("=" * 80)
