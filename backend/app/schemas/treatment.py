"""
Pydantic Schemas for Treatment Guidance & Disease Placeholder
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TreatmentItem(BaseModel):
    id: int
    crop: str
    condition: str
    category: str
    severity: str
    treatment: str
    preventive_measure: str
    precautions: str
    timing: str

class TreatmentResponse(BaseModel):
    total_records: int
    treatments: List[TreatmentItem]

class DiseasePlaceholderResponse(BaseModel):
    status: str
    module_name: str
    message: str
    is_placeholder: bool
    future_spec: Dict[str, Any]
