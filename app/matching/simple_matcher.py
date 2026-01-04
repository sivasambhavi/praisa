"""
Simple Patient Matcher - Combined Matching Engine

This module combines all 3 matching strategies (ABHA, Phonetic, Fuzzy) using waterfall logic.
It's the main matching engine used by the PRAISA API.

Waterfall Logic:
1. Try ABHA exact match first (highest confidence: 100%)
2. If no ABHA match, try phonetic match (high confidence: 90%)
3. If no phonetic match, try fuzzy match (medium confidence: 80-100%)
4. If fuzzy score 60-79%, flag for manual review (low confidence)
5. If score <60%, return no match

This approach ensures we use the most reliable matching method available.

Author: Senior Engineer
Date: 2026-01-04
"""

from app.matching.abha_match import abha_exact_match
from app.matching.phonetic_match import phonetic_match_indian
from app.matching.fuzzy_match import fuzzy_match
from app.matching.ml_matcher import MLPatientMatcher

# Initialize the global ML matcher (loads weights from disk if available)
ml_matcher = MLPatientMatcher()


def match_patients(patient_a: dict, patient_b: dict) -> dict:
    """
    Match two patients using combined matching strategies with waterfall logic.

    This function tries multiple matching strategies in order of reliability:
    1. ABHA exact match (government ID) - most reliable
    2. Phonetic match (Indian names) - handles transliteration
    3. Fuzzy match (string similarity) - handles typos

    The function stops at the first successful match (waterfall pattern).
    All strategy results are included in the response for transparency.

    Waterfall logic (stops at first match):
    1. ABHA exact match → 100% if match (highest confidence)
    2. Phonetic match on names → 90% if match (high confidence)
    3. Fuzzy match on names → score if >= 80% (medium confidence)
    4. Fuzzy match 60-79% → flag for review (low confidence)
    5. No match → 0% (no confidence)

    Args:
        patient_a: First patient dictionary with fields:
                  {patient_id, name, abha_number, dob, mobile, etc.}
        patient_b: Second patient dictionary with same fields

    Returns:
        dict: {
            "match_score": float (0-100) - Overall match confidence,
            "confidence": str (high/medium/low/none) - Confidence level,
            "method": str (ABHA_EXACT/PHONETIC_INDIAN/FUZZY/NONE) - Which strategy matched,
            "recommendation": str (MATCH/REVIEW/NO_MATCH) - Action to take,
            "patient_a_id": str - ID of first patient,
            "patient_b_id": str - ID of second patient,
            "details": dict - Full results from all 3 strategies
        }

    Examples:
        >>> # ABHA match (highest confidence)
        >>> match_patients(
        ...     {"patient_id": "HA001", "name": "Ramesh", "abha_number": "12-3456-7890-1234"},
        ...     {"patient_id": "HB001", "name": "Ramehs", "abha_number": "12-3456-7890-1234"}
        ... )
        {'match_score': 100.0, 'method': 'ABHA_EXACT', 'recommendation': 'MATCH', ...}

        >>> # Phonetic match (no ABHA, but names match phonetically)
        >>> match_patients(
        ...     {"patient_id": "HA002", "name": "Vijay Kumar", "abha_number": None},
        ...     {"patient_id": "HB002", "name": "Wijay Kumar", "abha_number": None}
        ... )
        {'match_score': 90.0, 'method': 'PHONETIC_INDIAN', 'recommendation': 'MATCH', ...}
    """
    # Extract patient IDs for response (use 'UNKNOWN' if missing)
    patient_a_id = patient_a.get("patient_id", "UNKNOWN")
    patient_b_id = patient_b.get("patient_id", "UNKNOWN")

    # Step 1: Run ML Decision Engine
    # The ML model extracts features (ABHA, Phonetic, Fuzzy, DOB, etc.) 
    # and returns a probability based on learned weights.
    ml_res = ml_matcher.predict_detailed(patient_a, patient_b)
    
    match_score = ml_res["prob"] * 100
    method = ml_res["method"]
    matched_fields = ml_res["matched_fields"]

    # Step 2: Determine confidence and recommendation based on ML score
    if match_score >= 80:
        confidence = "high"
        recommendation = "MATCH"
    elif match_score >= 60:
        confidence = "medium"
        recommendation = "REVIEW"
    else:
        confidence = "none"
        recommendation = "NO_MATCH"

    # Step 3: Return comprehensive result
    return {
        "match_score": match_score,
        "confidence": confidence,
        "method": method,
        "recommendation": recommendation,
        "matched_fields": matched_fields,
        "patient_a_id": patient_a_id,
        "patient_b_id": patient_b_id,
        "details": {
            "ml_result": ml_res,
            "is_ml_driven": True
        },
    }
