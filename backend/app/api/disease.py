"""
Disease Detection Integration Placeholder Endpoints
Compliance with Section 1, 7, 22, 23:
Model development is ON HOLD and being developed by team member.
This module provides a clean architectural contract for future EfficientNet-B0 drop-in.
No fake predictions are generated.
"""
from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from backend.app.schemas.treatment import DiseasePlaceholderResponse
from backend.app.services.treatment_service import TreatmentService

router = APIRouter(prefix="/disease", tags=["Disease Detection (Under Integration)"])

@router.get("/status", response_model=DiseasePlaceholderResponse)
def get_disease_module_status():
    """Returns current architecture integration status of the disease detection module."""
    return TreatmentService.get_placeholder_disease_response()

@router.post("/predict", response_model=DiseasePlaceholderResponse)
async def predict_crop_disease(
    image: Optional[UploadFile] = File(None, description="Leaf image file"),
    crop: Optional[str] = Form(None, description="Optional crop name")
):
    """
    Clean architectural placeholder endpoint for future EfficientNet-B0 model.
    Accepts image upload, validates payload, and informs client that model integration is underway.
    Does NOT fabricate fake predictions.
    """
    return TreatmentService.get_placeholder_disease_response(crop=crop)
