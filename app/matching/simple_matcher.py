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
    patient_a_id = patient_a.get('patient_id', 'UNKNOWN')
    patient_b_id = patient_b.get('patient_id', 'UNKNOWN')
    
    # Step 1: Run all 3 matching strategies
    # We run all strategies to provide complete details in the response,
    # even though we'll use only the first successful match
    
    # Strategy 1: ABHA exact match (government health ID)
    abha_result = abha_exact_match(patient_a, patient_b)
    
    # Strategy 2: Phonetic match (Indian name variations)
    phonetic_result = phonetic_match_indian(
        patient_a.get('name', ''),  # Extract name, default to empty string
        patient_b.get('name', '')
    )
    
    # Strategy 3: Fuzzy match (string similarity)
    fuzzy_result = fuzzy_match(
        patient_a.get('name', ''),
        patient_b.get('name', '')
    )
    
    # Step 2: Apply waterfall logic to determine final match result
    # We check strategies in order of reliability and stop at first match
    
    if abha_result['matched']:
        # Case 1: ABHA exact match - HIGHEST CONFIDENCE
        # Government-issued health ID matched exactly
        # This is 100% certain - same person
        match_score = abha_result['score']  # 100.0
        method = abha_result['method']  # "ABHA_EXACT"
        confidence = 'high'
        recommendation = 'MATCH'
        
    elif phonetic_result['matched']:
        # Case 2: Phonetic match - HIGH CONFIDENCE
        # Names match phonetically after Indian transliteration rules
        # Example: "Ramesh" matches "Ramehs", "Vijay" matches "Wijay"
        match_score = phonetic_result['score']  # 90.0
        method = phonetic_result['method']  # "PHONETIC_INDIAN"
        confidence = 'high'
        recommendation = 'MATCH'
        
    elif fuzzy_result['matched']:
        # Case 3: Fuzzy match >= 80% - MEDIUM CONFIDENCE
        # String similarity is high enough to suggest same person
        # Handles typos and minor variations
        match_score = fuzzy_result['score']  # 80-100
        method = fuzzy_result['method']  # "FUZZY"
        confidence = 'medium'
        recommendation = 'MATCH'
        
    elif fuzzy_result['score'] >= 60:
        # Case 4: Fuzzy match 60-79% - LOW CONFIDENCE
        # Some similarity but not enough to auto-match
        # Flag for manual review by hospital staff
        match_score = fuzzy_result['score']  # 60-79
        method = fuzzy_result['method']  # "FUZZY"
        confidence = 'low'
        recommendation = 'REVIEW'  # Needs human verification
        
    else:
        # Case 5: No match - NO CONFIDENCE
        # All strategies failed to find a match
        # These are likely different patients
        match_score = 0.0
        method = 'NONE'
        confidence = 'none'
        recommendation = 'NO_MATCH'
    
    # Step 3: Return comprehensive result
    # Include both the final decision and all strategy details for transparency
    return {
        "match_score": match_score,  # Final score (0-100)
        "confidence": confidence,  # Confidence level
        "method": method,  # Which strategy was used
        "recommendation": recommendation,  # What action to take
        "patient_a_id": patient_a_id,  # First patient ID
        "patient_b_id": patient_b_id,  # Second patient ID
        "details": {  # Full results from all strategies (for debugging/audit)
            "abha_result": abha_result,
            "phonetic_result": phonetic_result,
            "fuzzy_result": fuzzy_result
        }
    }

