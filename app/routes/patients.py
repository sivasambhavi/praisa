from fastapi import APIRouter, HTTPException, Query
from app.database import db

router = APIRouter()

@router.get("/patients/search")
async def search_patients(
    name: str = Query(None, min_length=2),
    abha: str = Query(None, min_length=14)
):
    """
    Search patients by Name (partial match) or ABHA Number (exact match).
    At least one parameter is required.
    """
    if not name and not abha:
        raise HTTPException(status_code=400, detail="Provide either 'name' or 'abha' query parameter")
    
    patients = db.search_patients(name=name, abha=abha)
    return {"results": patients, "count": len(patients)}

@router.get("/patients/{patient_id}")
async def get_patient_details(patient_id: str):
    """Get unique patient details by ID"""
    patient = db.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
    return patient

@router.get("/patients/{patient_id}/history")
async def get_patient_history(patient_id: str):
    """Get full visit history for a patient"""
    patient = db.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
        
    visits = db.get_patient_visits(patient_id)
    return {
        "patient": patient,
        "visits": visits,
        "visit_count": len(visits)
    }
