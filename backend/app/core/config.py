"""
Core Configuration for KrishiRakshak
Reads environment variables with graceful defaults.
Supports DATA_MODE: 'dataset' or 'live'.
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "KrishiRakshak"
    TAGLINE: str = "Predict. Detect. Irrigate. Protect."
    VERSION: str = "1.0.0"
    
    # Mode: 'dataset' (default for offline/college demo) or 'live'
    DATA_MODE: str = os.getenv("DATA_MODE", "dataset")
    
    # Weather API Key (OpenWeatherMap or WeatherAPI)
    WEATHER_API_KEY: Optional[str] = os.getenv("WEATHER_API_KEY", "")
    WEATHER_API_PROVIDER: str = os.getenv("WEATHER_API_PROVIDER", "openweathermap") # or "weatherapi"
    WEATHER_CITY: str = os.getenv("WEATHER_CITY", "Nagpur")
    
    # Database URL: defaults to PostgreSQL, with auto-fallback to SQLite for seamless local demo
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/krishirakshak")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "krishirakshak-super-secret-academic-key-2026")
    
    # Paths
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    DATA_DIR: str = os.path.join(BASE_DIR, "data/raw")
    MODELS_DIR: str = os.path.join(BASE_DIR, "backend/ml/models")

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
