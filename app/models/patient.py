from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class PatientBase(BaseModel):
    id: str
    name: str = Field(..., description="Patient's full name")
    dob: str = Field(..., description="Date of birth in YYYY-MM-DD")
    gender: str
    phone: Optional[str] = None
    email: Optional[str] = None
    abha_number: Optional[str] = Field(None, description="Ayushman Bharat Health Account Number")
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    hospital_id: str

    class Config:
        from_attributes = True
