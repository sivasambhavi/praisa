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

# Create API router for patient endpoints
# This router will be included in main.py with prefix "/api"
router = APIRouter()


@router.get("/patients/search")
async def search_patients(
    name: str = Query(None, min_length=2),  # Name search (min 2 chars)
    abha: str = Query(None, min_length=14)  # ABHA search (min 14 chars)
):
    """
    Search for patients by name or ABHA number.
    
    Supports two search modes:
    1. Name search: Partial, case-insensitive match (e.g., "Ram" matches "Ramesh")
    2. ABHA search: Exact match on government health ID
    
    At least one parameter must be provided.
    
    Query Parameters:
        name: Patient name (partial match, min 2 characters)
        abha: ABHA number (exact match, min 14 characters)
    
    Returns:
        {
            "results": [...],  # List of matching patients
            "count": int       # Number of results
        }
    
    Raises:
        HTTPException 400: If neither name nor abha is provided
    
    Examples:
        GET /api/patients/search?name=Ramesh
        GET /api/patients/search?abha=12-3456-7890-1234
    """
    # Validate that at least one search parameter is provided
    if not name and not abha:
        raise HTTPException(
            status_code=400, 
            detail="Provide either 'name' or 'abha' query parameter"
        )
    
    # Call database search function
    # Returns list of patient dictionaries
    patients = db.search_patients(name=name, abha=abha)
    
    # Return results with count
    return {
        "results": patients,
        "count": len(patients)
    }


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
        raise HTTPException(
            status_code=404, 
            detail=f"Patient {patient_id} not found"
        )
    
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
        raise HTTPException(
            status_code=404, 
            detail=f"Patient {patient_id} not found"
        )
    
    # Get all visits for this patient
    # Visits are ordered by admission_date DESC (most recent first)
    visits = db.get_patient_visits(patient_id)
    
    # Return comprehensive response
    return {
        "patient": patient,           # Patient information
        "visits": visits,             # Visit history
        "visit_count": len(visits)    # Total visits
    }

