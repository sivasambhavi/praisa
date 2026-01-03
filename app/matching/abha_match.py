"""
ABHA Exact Matching

Senior Engineer: Implement using Antigravity prompt from docs/SENIOR_ENGINEER_DEMO_PRD.md

TODO:
1. Function: abha_exact_match(patient_a: dict, patient_b: dict) -> dict
2. Check if ABHA numbers match
3. Return 100% if match, 0% if no match
4. Write 5 test cases in tests/test_abha_match.py
"""

def abha_exact_match(patient_a: dict, patient_b: dict) -> dict:
    """
    Match patients based on ABHA number exact match.
    
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
    # TODO: Implement ABHA exact matching logic
    pass
