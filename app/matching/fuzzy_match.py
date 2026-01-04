"""
Fuzzy Name Matching

Uses RapidFuzz library for fuzzy string matching to handle typos and variations.
"""

from rapidfuzz import fuzz


def fuzzy_match(name1: str, name2: str) -> dict:
    """
    Match names using fuzzy string matching.
    
    Uses RapidFuzz's token_sort_ratio which:
    - Handles word order differences
    - Handles typos and minor variations
    - Returns similarity score 0-100
    
    Args:
        name1: First name
        name2: Second name
    
    Returns:
        dict: {
            "score": float (0-100),
            "method": "FUZZY",
            "matched": bool (score >= 80),
            "details": str
        }
    """
    # Handle empty names
    if not name1 or not name2:
        return {
            "score": 0.0,
            "method": "FUZZY",
            "matched": False,
            "details": "One or both names are empty"
        }
    
    # Normalize: lowercase and strip whitespace
    name1_norm = name1.lower().strip()
    name2_norm = name2.lower().strip()
    
    # Calculate fuzzy similarity using token_sort_ratio
    # This handles word order and partial matches well
    score = fuzz.token_sort_ratio(name1_norm, name2_norm)
    
    # Consider it a match if score >= 80%
    matched = score >= 80.0
    
    return {
        "score": float(score),
        "method": "FUZZY",
        "matched": matched,
        "details": f"Fuzzy similarity: {score:.1f}% ({'MATCH' if matched else 'NO MATCH'})"
    }
