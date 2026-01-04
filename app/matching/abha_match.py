"""
ABHA Exact Matching Module

This module provides exact matching functionality for ABHA (Ayushman Bharat Health Account) numbers.
ABHA is India's government-issued unique health identifier, similar to a Social Security Number.

When both patients have ABHA numbers and they match exactly, it's a 100% certain match.
This is the highest confidence matching strategy in PRAISA.

Author: Senior Engineer
Date: 2026-01-04
"""


def abha_exact_match(patient_a: dict, patient_b: dict) -> dict:
    """
    Match patients based on ABHA number exact match.

    ABHA (Ayushman Bharat Health Account) is India's government-issued
    unique health ID. If both patients have ABHA numbers and they match,
    it's a 100% certain match.

    Args:
        patient_a: First patient dictionary with 'abha_number' field
        patient_b: Second patient dictionary with 'abha_number' field

    Returns:
        dict: {
            "score": float (0-100),
            "method": "ABHA_EXACT",
            "matched": bool,
            "details": str
        }
    """
    # Get ABHA numbers, handle None/missing values
    abha_a = patient_a.get("abha_number")
    abha_b = patient_b.get("abha_number")

    # If either ABHA is missing, we can't match on ABHA
    if not abha_a or not abha_b:
        return {
            "score": 0.0,
            "method": "ABHA_EXACT",
            "matched": False,
            "details": "ABHA number missing for one or both patients",
        }

    # Normalize ABHA numbers (remove spaces, hyphens, convert to lowercase)
    abha_a_normalized = str(abha_a).replace(" ", "").replace("-", "").lower().strip()
    abha_b_normalized = str(abha_b).replace(" ", "").replace("-", "").lower().strip()

    # Check if ABHA numbers match exactly
    if abha_a_normalized == abha_b_normalized:
        return {
            "score": 100.0,
            "method": "ABHA_EXACT",
            "matched": True,
            "details": f"ABHA numbers match: {abha_a}",
        }
    else:
        return {
            "score": 0.0,
            "method": "ABHA_EXACT",
            "matched": False,
            "details": f"ABHA numbers do not match: {abha_a} != {abha_b}",
        }
