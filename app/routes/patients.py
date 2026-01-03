from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.models.patient import Patient
from app.database.db import get_db_connection

router = APIRouter()

# Mock database access for now
def get_patient_from_db(patient_id: str):
    # This would be replaced by actual DB call
    mock_patients = {
        "HA001": {"id": "HA001", "name": "Ramesh Singh", "dob": "1985-03-15", "gender": "M", "abha_number": "12-3456-7890-1234", "hospital_id": "A"},
        "HB001": {"id": "HB001", "name": "Ramehs Singh", "dob": "1985-03-15", "gender": "M", "abha_number": "12-3456-7890-1234", "hospital_id": "B"},
    }
    return mock_patients.get(patient_id)

@router.get("/{patient_id}", response_model=Patient)
async def get_patient(patient_id: str):
    patient = get_patient_from_db(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.get("/search/", response_model=List[Patient])
async def search_patients(name: str, hospital_id: str):
    # Mock search
    if "ramesh" in name.lower() and hospital_id == "A":
        return [get_patient_from_db("HA001")]
    return []
