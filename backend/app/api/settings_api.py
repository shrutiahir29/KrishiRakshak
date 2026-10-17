"""
System Settings and API Configuration Endpoints
Allows inspection and dynamic adjustment of runtime modes without exposing secrets.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any
from backend.app.core.config import settings

router = APIRouter(prefix="/settings", tags=["Settings & Configuration"])

class SettingsUpdateRequest(BaseModel):
    data_mode: Optional[str] = None # 'dataset' or 'live'
    weather_api_key: Optional[str] = None
    weather_city: Optional[str] = None

@router.get("/")
def get_system_settings() -> Dict[str, Any]:
    """Returns current environment configuration and component statuses."""
    has_key = bool(settings.WEATHER_API_KEY and len(settings.WEATHER_API_KEY.strip()) > 5)
    return {
        "project_name": settings.PROJECT_NAME,
        "tagline": settings.TAGLINE,
        "version": settings.VERSION,
        "data_mode": settings.DATA_MODE,
        "weather_api_configured": has_key,
        "weather_api_provider": settings.WEATHER_API_PROVIDER,
        "weather_city": settings.WEATHER_CITY,
        "active_mode_badge": "LIVE WEATHER MODE" if (settings.DATA_MODE == "live" and has_key) else "DATASET MODE",
        "database_backend": "PostgreSQL (Configured with automated SQLite local fallback)",
        "hardware_abstraction": {
            "active_provider": "DatasetProvider",
            "future_sensor_provider": "LiveSensorProvider (ESP32 Ready)"
        },
        "disease_detection_status": "ON HOLD (EfficientNet-B0 interface ready)"
    }

@router.post("/")
def update_system_settings(payload: SettingsUpdateRequest) -> Dict[str, Any]:
    """Dynamically updates runtime settings for the current session."""
    if payload.data_mode:
        settings.DATA_MODE = payload.data_mode.lower()
    if payload.weather_api_key is not None:
        settings.WEATHER_API_KEY = payload.weather_api_key.strip()
    if payload.weather_city:
        settings.WEATHER_CITY = payload.weather_city.strip()

    has_key = bool(settings.WEATHER_API_KEY and len(settings.WEATHER_API_KEY.strip()) > 5)
    return {
        "status": "success",
        "message": "Settings updated successfully",
        "data_mode": settings.DATA_MODE,
        "weather_api_configured": has_key,
        "active_mode_badge": "LIVE WEATHER MODE" if (settings.DATA_MODE == "live" and has_key) else "DATASET MODE"
    }
