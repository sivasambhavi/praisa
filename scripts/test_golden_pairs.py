"""
Test All Golden Pairs Script

Comprehensive testing of all 5 golden pairs with detailed output.
Tests both ABHA matching and phonetic matching independently.

Usage:
    python scripts/test_golden_pairs.py

Author: Senior Engineer
Date: 2026-01-04
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database.db import get_patient
from app.matching.simple_matcher import match_patients
from app.matching.phonetic_match import phonetic_match_indian


# Golden pairs from the database
GOLDEN_PAIRS = [
    ("HA001", "HB001", "Ramesh Singh", "Ramehs Singh", "Typo in name"),
    ("HA002", "HB002", "Priya Sharma", "Prya Sharma", "Dropped vowel"),
    ("HA003", "HB003", "Vijay Kumar", "Wijay Kumar", "v->w transliteration"),
    ("HA004", "HB004", "Amit Kumar", "Amit Kumarr", "Extra r"),
    ("HA005", "HB005", "Sunita Gupta", "Suneeta Gupta", "Vowel variation i->ee"),
]


def test_combined_matching():
    """Test combined matching (ABHA + Phonetic + Fuzzy)"""
    print("=" * 80)
    print("PRAISA - Combined Matching Test (All Strategies)")
    print("=" * 80)
    print()

    passed = 0
    failed = 0

    for ha_id, hb_id, name_a, name_b, description in GOLDEN_PAIRS:
        # Get patients from database
        patient_a = get_patient(ha_id)
        patient_b = get_patient(hb_id)

        if not patient_a or not patient_b:
            print(f"[XX] {ha_id} or {hb_id} not found in database")
            failed += 1
            continue

        # Match patients
        result = match_patients(patient_a, patient_b)

        # Check if match score is acceptable (>= 90%)
        if result["match_score"] >= 90:
            status = "[OK]"
            passed += 1
        else:
            status = "[!!]"
            failed += 1

        print(f"{status} {ha_id} ({name_a:20s}) <-> {hb_id} ({name_b:20s})")
        score = result["match_score"]
        method = result["method"]
        recommendation = result["recommendation"]
        print(f"   Score: {score:5.1f}% | Method: {method:20s} | {recommendation}")
        print(f"   Description: {description}")
        print()

    return passed, failed


def test_phonetic_only():
    """Test phonetic matching independently (without ABHA)"""
    print("=" * 80)
    print("PRAISA - Phonetic Matching Test (WOW FACTOR)")
    print("=" * 80)
    print()

    passed = 0
    failed = 0

    for ha_id, hb_id, name_a, name_b, description in GOLDEN_PAIRS:
        # Test phonetic matching directly
        result = phonetic_match_indian(name_a, name_b)

        if result["matched"]:
            status = "[OK]"
            passed += 1
        else:
            status = "[XX]"
            failed += 1

        print(f"{status} {name_a:20s} <-> {name_b:20s}")
        print(f"   Score: {result['score']:5.1f}% | {description}")
        print(f"   Details: {result['details']}")
        print()

    return passed, failed


def main():
    """Run all tests"""
    print()

    # Test 1: Combined matching
    combined_passed, combined_failed = test_combined_matching()

    # Test 2: Phonetic matching only
    phonetic_passed, phonetic_failed = test_phonetic_only()

    # Summary
    print("=" * 80)
    print("Test Summary")
    print("=" * 80)
    print(f"Combined Matching: {combined_passed}/5 passed, {combined_failed}/5 failed")
    print(f"Phonetic Matching: {phonetic_passed}/5 passed, {phonetic_failed}/5 failed")
    print()

    if combined_failed == 0 and phonetic_failed == 0:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
