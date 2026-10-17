"""
Pydantic Schemas for Weather Module
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class CurrentWeatherResponse(BaseModel):
    location: str
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Relative Humidity percentage")
    rainfall: float = Field(..., description="Precipitation in mm")
    wind_speed: float = Field(..., description="Wind speed in m/s")
    weather_condition: str
    timestamp: str
    data_source: str
    mode_badge: str
    notes: Optional[str] = None

class ForecastDay(BaseModel):
    date: str
    day_name: str
    temperature: float
    temp_min: float
    temp_max: float
    humidity: float
    rainfall_mm: float
    pop_percent: int
    condition: str

class ForecastResponse(BaseModel):
    location: str
    mode_badge: str
    data_source: str
    upcoming_48h_rain_mm: float
    forecast: List[ForecastDay]
