from pydantic import BaseModel
from typing import Optional, List
from app.models.patient import Patient


class MatchRequest(BaseModel):
    source_patient_id: str
    target_hospital_id: str


class MatchResult(BaseModel):
    source_patient: Patient
    target_patient: Optional[Patient]
    match_score: int
    match_method: str
    confidence: str
    matched_fields: List[str]
    unified_history_available: bool
