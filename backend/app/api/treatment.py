"""
Treatment Guidance API Endpoints
"""
from fastapi import APIRouter, Query
from typing import Optional, List, Dict, Any
from backend.app.schemas.treatment import TreatmentResponse
from backend.app.services.treatment_service import TreatmentService

router = APIRouter(prefix="/treatment", tags=["Treatment Guidance"])

@router.get("/", response_model=TreatmentResponse)
def get_treatments(
    crop: Optional[str] = Query(None, description="Optional crop filter"),
    condition: Optional[str] = Query(None, description="Optional condition or pest name")
):
    """Returns IPM treatments, optionally filtered by crop or condition."""
    if condition:
        data = TreatmentService.find_treatment(query=condition, crop=crop)
    elif crop:
        data = TreatmentService.get_treatments_by_crop(crop=crop)
    else:
        data = TreatmentService.get_all_treatments()
    return {
        "total_records": len(data),
        "treatments": data
    }

@router.get("/all", response_model=TreatmentResponse)
def get_all_treatments():
    """Returns the complete agricultural IPM treatment knowledge base."""
    data = TreatmentService.get_all_treatments()
    return {
        "total_records": len(data),
        "treatments": data
    }

@router.get("/{condition}")
def search_treatment(
    condition: str,
    crop: Optional[str] = Query(None, description="Optional crop filter")
) -> List[Dict[str, Any]]:
    """Looks up recommended IPM treatments for a specific pest or condition."""
    return TreatmentService.find_treatment(query=condition, crop=crop)
