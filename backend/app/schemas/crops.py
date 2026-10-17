"""
Pydantic Schemas for Crop Recommendation Module
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class CropRecommendRequest(BaseModel):
    N: float = Field(..., ge=0.0, le=250.0, description="Nitrogen ratio in kg/ha")
    P: float = Field(..., ge=0.0, le=250.0, description="Phosphorus ratio in kg/ha")
    K: float = Field(..., ge=0.0, le=250.0, description="Potassium ratio in kg/ha")
    temperature: float = Field(..., ge=-10.0, le=55.0, description="Temperature in °C")
    humidity: float = Field(..., ge=0.0, le=100.0, description="Relative humidity in %")
    ph: float = Field(..., ge=2.0, le=11.0, description="Soil pH")
    rainfall: float = Field(..., ge=0.0, le=500.0, description="Rainfall in mm")
    top_k: Optional[int] = Field(5, ge=1, le=10, description="Number of recommendations to return")

class CropScoreItem(BaseModel):
    crop: str
    crop_code: str
    score: float
    sub_scores: Dict[str, float]
    reasons: List[str]
    optimal_conditions: Dict[str, str]

class CropRecommendResponse(BaseModel):
    method: str
    total_evaluated: int
    recommendations: List[CropScoreItem]
    input_conditions: Dict[str, float]
    timestamp: str
