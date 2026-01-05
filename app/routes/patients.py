"""
Patient API Routes

This module provides REST API endpoints for patient data operations.
Includes search, details retrieval, and visit history endpoints.

Endpoints:
- GET /api/patients/search - Search patients by name or ABHA
- GET /api/patients/{id} - Get patient details
- GET /api/patients/{id}/history - Get patient visit history

Author: Mid Engineer
Date: 2026-01-04
"""

from fastapi import APIRouter, HTTPException, Query
from app.database import db
from app.utils.quality_scorer import calculate_data_quality

# Create API router for patient endpoints
# This router will be included in main.py with prefix "/api"
router = APIRouter()


@router.get("/patients/search")
async def search_patients(
    name: str = Query(None, min_length=2),  # Name search (min 2 chars)
    abha: str = Query(None, min_length=5),  # ABHA search (min 5 chars for flexibility)
    aadhaar: str = Query(None, min_length=12),  # Aadhaar search (min 12 chars)
    phone: str = Query(None, min_length=10),  # Phone search (min 10 digits)
    hospital_id: str = Query(None),  # Optional hospital filter
):
    """
    Search for patients by name, ABHA, Aadhaar, or phone number.

    CROSS-HOSPITAL SEARCH: When searching by ABHA, Aadhaar, or phone, automatically searches
    across ALL hospitals and returns exact matches, enabling cross-hospital patient identification.

    Supports four search modes:
    1. Name search: Partial, case-insensitive match (e.g., "Ram" matches "Ramesh")
    2. ABHA search: Exact match on government health ID (CROSS-HOSPITAL)
    3. Aadhaar search: Exact match on UIDAI ID (CROSS-HOSPITAL)
    4. Phone search: Exact match on mobile number (CROSS-HOSPITAL)

    At least one parameter must be provided.

    Query Parameters:
        name: Patient name (partial match, min 2 characters)
        abha: ABHA number (exact match across ALL hospitals, min 5 characters)
        aadhaar: Aadhaar number (exact match across ALL hospitals, min 12 digits)
        phone: Phone/mobile number (exact match across ALL hospitals, min 10 digits)
        hospital_id: Optional hospital filter (only applies to name search)

    Returns:
        {
            "results": [...],  # List of matching patients
            "count": int,      # Number of results
            "search_type": str # "abha", "aadhaar", "phone", or "name"
        }

    Raises:
        HTTPException 400: If no search parameter is provided

    Examples:
        GET /api/patients/search?name=Ramesh&hospital_id=hospital_a
        GET /api/patients/search?abha=12-3456-7890-1234
        GET /api/patients/search?aadhaar=123412341234
        GET /api/patients/search?phone=9876543210
    """
    # Validate that at least one search parameter is provided
    if not name and not abha and not phone and not aadhaar:
        raise HTTPException(
            status_code=400,
            detail="Provide 'name', 'abha', 'aadhaar', or 'phone' query parameter",
        )

    # Priority: ABHA > Aadhaar > Phone > Name (most specific to least specific)
    search_type = "name"

    if abha:
        # ABHA match - highest priority, searches ALL hospitals automatically
        search_type = "abha"
        patients = db.search_patients(
            abha=abha, hospital_id=None
        )  # Force cross-hospital
    elif aadhaar:
        # Aadhaar match - searches ALL hospitals automatically
        search_type = "aadhaar"
        # Clean aadhaar (remove spaces, dashes)
        clean_aadhaar = aadhaar.replace("-", "").replace(" ", "").strip()
        patients = db.search_patients(aadhaar=clean_aadhaar, hospital_id=None)
    elif phone:
        # Phone match - search ALL hospitals automatically
        search_type = "phone"
        # Clean phone number (remove +91, spaces, dashes)
        clean_phone = phone.replace("+91", "").replace("-", "").replace(" ", "").strip()
        patients = db.search_patients(
            phone=clean_phone, hospital_id=None
        )  # Force cross-hospital
    else:
        # Name search - respects hospital filter
        search_type = "name"
        patients = db.search_patients(name=name, hospital_id=hospital_id)

    # Calculate data quality for each result
    for p in patients:
        score, missing = calculate_data_quality(p)
        p["quality_score"] = score
        p["missing_fields"] = missing

    # Return results with search type indicator
    return {"results": patients, "count": len(patients), "search_type": search_type}


@router.get("/patients/{patient_id}")
async def get_patient_details(patient_id: str):
    """
    Get detailed information for a specific patient.

    Retrieves complete patient record including:
    - Personal information (name, DOB, gender)
    - Contact details (mobile, address)
    - ABHA health ID
    - Hospital affiliation

    Path Parameters:
        patient_id: Unique patient identifier (e.g., "HA001", "HB001")

    Returns:
        Patient dictionary with all fields

    Raises:
        HTTPException 404: If patient not found

    Example:
        GET /api/patients/HA001

        Response:
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
    # Query database for patient
    patient = db.get_patient(patient_id)

    # Return 404 if patient not found
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    # Calculate data quality
    score, missing = calculate_data_quality(patient)
    patient["quality_score"] = score
    patient["missing_fields"] = missing

    # Return patient data
    return patient


@router.get("/patients/{patient_id}/history")
async def get_patient_history(patient_id: str):
    """
    Get complete medical visit history for a patient.

    Retrieves:
    - Patient information
    - All visit records (ordered by most recent first)
    - Total visit count

    This endpoint is useful for:
    - Unified patient view across hospitals
    - Medical history review
    - Continuity of care

    Path Parameters:
        patient_id: Unique patient identifier

    Returns:
        {
            "patient": {...},      # Patient details
            "visits": [...],       # List of visits (newest first)
            "visit_count": int     # Total number of visits
        }

    Raises:
        HTTPException 404: If patient not found

    Example:
        GET /api/patients/HA001/history

        Response:
        {
            "patient": {"patient_id": "HA001", "name": "Ramesh Singh", ...},
            "visits": [
                {
                    "visit_id": "VA002",
                    "patient_id": "HA001",
                    "admission_date": "2025-12-20 14:30:00",
                    "visit_type": "OPD",
                    "diagnosis": "Diabetes Follow-up",
                    "doctor_name": "Dr. Anjali Mehta"
                },
                ...
            ],
            "visit_count": 2
        }
    """
    # First, verify patient exists
    patient = db.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    # Get all visits for this patient
    # Visits are ordered by admission_date DESC (most recent first)
    visits = db.get_patient_visits(patient_id)

    # Return comprehensive response
    return {
        "patient": patient,  # Patient information
        "visits": visits,  # Visit history
        "visit_count": len(visits),  # Total visits
    }
