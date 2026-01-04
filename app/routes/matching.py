"""
Matching API Routes

This module provides the REST API endpoint for patient matching.
Uses the simple_matcher module which combines ABHA, phonetic, and fuzzy matching.

Endpoint: POST /api/match
Purpose: Match two patient records using combined strategies

Author: Senior Engineer
Date: 2026-01-04
"""

from fastapi import APIRouter, HTTPException
from app.models.patient import MatchRequest, MatchResult
from app.matching.simple_matcher import match_patients

# Create API router for matching endpoints
# This router will be included in main.py with prefix "/api"
router = APIRouter()


@router.post("/match", response_model=MatchResult)
async def match_two_patients(request: MatchRequest):
    """
    Match two patients using combined matching strategies.
    
    This endpoint accepts two patient records and returns a match result
    using the waterfall matching logic (ABHA → Phonetic → Fuzzy).
    
    Tries 3 strategies in order of reliability:
    1. ABHA exact match (100% confidence)
    2. Phonetic match for Indian names (90% confidence)
    3. Fuzzy match (0-100% confidence)
    
    Request Body:
        {
            "patient_a": {
                "patient_id": "HA001",
                "name": "Ramesh Singh",
                "abha_number": "12-3456-7890-1234",
                ...
            },
            "patient_b": {
                "patient_id": "HB001",
                "name": "Ramehs Singh",
                "abha_number": "12-3456-7890-1234",
                ...
            }
        }
    
    Returns:
        MatchResult: {
            "match_score": 100.0,
            "confidence": "high",
            "method": "ABHA_EXACT",
            "recommendation": "MATCH",
            "patient_a_id": "HA001",
            "patient_b_id": "HB001",
            "details": {...}
        }
    
    Raises:
        HTTPException: 500 if matching algorithm fails
    """
    try:
        # Call the simple matcher with both patient records
        # This runs all 3 strategies and returns the best match
        result = match_patients(request.patient_a, request.patient_b)
        return result
        
    except Exception as e:
        # If any error occurs during matching, return 500 error
        # In production, we'd log this error for debugging
        raise HTTPException(
            status_code=500,
            detail=f"Error matching patients: {str(e)}"
        )

