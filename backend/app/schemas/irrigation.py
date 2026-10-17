"""
Pydantic Schemas for Smart Irrigation Module
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class IrrigationCurrentResponse(BaseModel):
    soil_moisture: float
    soil_moisture_percent: float
    temperature: float
    timestamp: str
    field_id: str
    sensor_id: str
    data_source: str
    reading_label: str

class IrrigationAdvisoryRequest(BaseModel):
    crop: str = Field("prei", description="Crop identifier")
    growth_stage: str = Field("mid", description="initial, mid, or late")
    soil_type: str = Field("Sdm", description="Soil classification code")
    irrigation_method: str = Field("druppel", description="druppel (drip) or haspel (sprinkler)")
    forecast_rain_48h: Optional[float] = Field(0.0, ge=0.0, description="Upcoming 48h precipitation in mm")
    manual_soil_moisture: Optional[float] = Field(None, ge=0.01, le=1.0, description="Optional manual override VWC")

class IrrigationAdvisoryResponse(BaseModel):
    decision: str # IRRIGATE or WAIT
    intensity: str # NONE, LOW, MODERATE, HIGH
    water_amount_mm: float
    water_liters_per_m2: float
    water_liters_per_hectare: int
    soil_moisture_vwc: float
    soil_moisture_percent: float
    depletion_percentage: float
    field_capacity_percent: float
    wilting_point_percent: float
    mad_threshold_percent: float
    eto_mm_day: float
    kc: float
    etc_mm_day: float
    forecast_rain_48h: float
    irrigation_method: str
    crop: str
    crop_name: str
    growth_stage: str
    soil_type: str
    data_source: str
    reading_label: str
    sensor_id: str
    timestamp: str
    reasons: List[str]
