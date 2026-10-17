"""
Weather API Endpoints for KrishiRakshak
"""
from fastapi import APIRouter, Query
from typing import Optional
from backend.app.schemas.weather import CurrentWeatherResponse, ForecastResponse
from backend.app.services.weather_service import weather_service

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/current", response_model=CurrentWeatherResponse)
async def get_current_weather(
    city: Optional[str] = Query(None, description="City or region name"),
    lat: Optional[float] = Query(None, description="Latitude coordinate"),
    lon: Optional[float] = Query(None, description="Longitude coordinate")
):
    """Retrieves current weather and live humidity from Live Weather API (or fallback)."""
    return await weather_service.get_current_weather(city=city, lat=lat, lon=lon)

@router.get("/forecast", response_model=ForecastResponse)
async def get_weather_forecast(
    city: Optional[str] = Query(None, description="City or region name"),
    lat: Optional[float] = Query(None, description="Latitude coordinate"),
    lon: Optional[float] = Query(None, description="Longitude coordinate")
):
    """Retrieves 3-5 day weather forecast with daily humidity from Live Weather API."""
    return await weather_service.get_forecast(city=city, lat=lat, lon=lon)
