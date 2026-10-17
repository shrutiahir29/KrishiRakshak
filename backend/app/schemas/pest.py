"""
Pydantic Schemas for Pest Forecasting Module
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class PestPredictRequest(BaseModel):
    temperature: float = Field(..., ge=-10.0, le=55.0, description="Temperature in °C")
    humidity: float = Field(..., ge=0.0, le=100.0, description="Relative humidity in %")
    rainfall: float = Field(..., ge=0.0, le=500.0, description="Rainfall in mm")
    crop: str = Field("cotton", description="Crop name (e.g. cotton, rice, maize, chickpea)")
    N: Optional[float] = Field(60.0, ge=0.0, le=250.0, description="Soil Nitrogen (kg/ha)")
    P: Optional[float] = Field(40.0, ge=0.0, le=250.0, description="Soil Phosphorus (kg/ha)")
    K: Optional[float] = Field(40.0, ge=0.0, le=250.0, description="Soil Potassium (kg/ha)")
    ph: Optional[float] = Field(6.5, ge=3.0, le=10.0, description="Soil pH")

class ShapContribution(BaseModel):
    feature: str
    label: str
    input_value: float
    shap_value: float
    impact: str
    contribution_sign: str
    description: str
    reasoning: str

class PestPredictResponse(BaseModel):
    predicted_risk: str # LOW, MEDIUM, HIGH
    probability: float
    probability_percent: float
    forecast_window: str # "3-5 days ahead"
    crop: str
    input_features: Dict[str, Any]
    class_probabilities: Dict[str, float]
    shap_explanations: List[ShapContribution]
    top_drivers: List[str]
    action_summary: str
    model_version: str
    timestamp: str

class PestHistoryItem(BaseModel):
    id: int
    timestamp: str
    crop: str
    predicted_risk: str
    probability: float
    temperature: float
    humidity: float
    rainfall: float
