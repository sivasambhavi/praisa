"""
Pydantic Models for PRAISA API

Data validation models for patient matching API.
Uses Pydantic for automatic validation, serialization, and API documentation.

Models:
- PatientModel: Patient data structure
- MatchRequest: Request body for matching endpoint
- MatchResult: Response structure for matching endpoint

Author: Senior Engineer
Date: 2026-01-04
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class PatientModel(BaseModel):
    """
    Patient data model for API requests and responses.

    Represents a patient record with all relevant fields.
    All fields except 'name' are optional to support partial data.

    Fields:
        patient_id: Unique identifier (e.g., "HA001", "HB001")
        hospital_id: Hospital identifier (e.g., "hospital_a")
        name: Patient full name (required)
        dob: Date of birth in YYYY-MM-DD format
        mobile: Mobile phone number
        gender: Gender (M/F/Other)
        abha_number: ABHA health ID (government-issued)
        address: Full residential address
        state: State/province name

    Example:
        {
            "patient_id": "HA001",
            "hospital_id": "hospital_a",
            "name": "Ramesh Singh",
            "dob": "1985-03-15",
            "mobile": "9876543210",
            "gender": "M",
            "abha_number": "12-3456-7890-1234",
            "address": "123 MG Road Mumbai",
            "state": "Maharashtra"
        }
    """

    patient_id: Optional[str] = None  # Unique patient identifier
    hospital_id: Optional[str] = None  # Hospital affiliation
    name: str  # Patient name (required)
    dob: Optional[str] = None  # Date of birth
    mobile: Optional[str] = None  # Contact number
    gender: Optional[str] = None  # Gender
    abha_number: Optional[str] = None  # Government health ID
    address: Optional[str] = None  # Residential address
    state: Optional[str] = None  # State/province

    # Data Quality Fields
    quality_score: Optional[int] = Field(
        None, description="Data completeness score (0-100)"
    )
    missing_fields: Optional[list[str]] = Field(
        None, description="List of missing critical fields"
    )


class MatchRequest(BaseModel):
    """
    Request body for patient matching endpoint.

    Contains two patient records to be compared using the matching algorithms.
    Patients can be provided as dictionaries with any subset of fields.

    Fields:
        patient_a: First patient data (dict)
        patient_b: Second patient data (dict)

    Example:
        {
            "patient_a": {
                "patient_id": "HA001",
                "name": "Ramesh Singh",
                "abha_number": "12-3456-7890-1234"
            },
            "patient_b": {
                "patient_id": "HB001",
                "name": "Ramehs Singh",
                "abha_number": "12-3456-7890-1234"
            }
        }
    """

    patient_a: Dict[str, Any] = Field(
        ..., description="First patient data to compare"  # Required field
    )
    patient_b: Dict[str, Any] = Field(
        ..., description="Second patient data to compare"  # Required field
    )


class MatchResult(BaseModel):
    """
    Match result response from matching endpoint.

    Contains the overall match result plus detailed results from all strategies.
    Provides transparency into how the match decision was made.

    Fields:
        match_score: Overall match score (0-100)
        confidence: Confidence level (high/medium/low/none)
        method: Which strategy was used (ABHA_EXACT/PHONETIC_INDIAN/FUZZY/NONE)
        recommendation: Action to take (MATCH/REVIEW/NO_MATCH)
        patient_a_id: ID of first patient
        patient_b_id: ID of second patient
        details: Full results from all 3 strategies

    Example:
        {
            "match_score": 100.0,
            "confidence": "high",
            "method": "ABHA_EXACT",
            "recommendation": "MATCH",
            "patient_a_id": "HA001",
            "patient_b_id": "HB001",
            "details": {
                "abha_result": {"score": 100.0, "matched": true, ...},
                "phonetic_result": {"score": 90.0, "matched": true, ...},
                "fuzzy_result": {"score": 95.0, "matched": true, ...}
            }
        }
    """

    match_score: float = Field(
        ..., description="Overall match score (0-100)"  # Required
    )
    confidence: str = Field(
        ..., description="Confidence level: high/medium/low/none"  # Required
    )
    method: str = Field(
        ...,  # Required
        description="Matching method used: ABHA_EXACT/PHONETIC_INDIAN/FUZZY/NONE",
    )
    recommendation: str = Field(
        ..., description="Recommended action: MATCH/REVIEW/NO_MATCH"  # Required
    )
    patient_a_id: str  # First patient identifier
    patient_b_id: str  # Second patient identifier
    matched_fields: Optional[list[str]] = Field(
        None, description="List of fields that the AI identified as matching"
    )
    details: Dict[str, Any] = Field(
        ..., description="Detailed results from all matching strategies"  # Required
    )
