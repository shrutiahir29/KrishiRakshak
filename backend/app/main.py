"""
KRISHIRAKSHAK — FastAPI Application Entry Point
AI-Based Weather-Driven Pest Forecasting, Smart Irrigation, and Crop Recommendation System
Tagline: "Predict. Detect. Irrigate. Protect."
"""
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure root is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.app.core.config import settings
from backend.app.core.database import engine, Base
from backend.app.models.models import * # register all models with Base
from backend.app.api.weather import router as weather_router
from backend.app.api.pest import router as pest_router
from backend.app.api.irrigation import router as irrigation_router
from backend.app.api.crops import router as crops_router
from backend.app.api.treatment import router as treatment_router
from backend.app.api.disease import router as disease_router
from backend.app.api.analytics import router as analytics_router
from backend.app.api.settings_api import router as settings_router

# Initialize database schema tables
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized successfully.")
except Exception as e:
    print(f"Notice: Database initialization deferred or encountered: {e}")

app = FastAPI(
    title="KRISHIRAKSHAK API",
    description="AI-Based Weather-Driven Pest Forecasting, Smart Irrigation, and Crop Recommendation System",
    version=settings.VERSION
)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow all for local dev & college presentation
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register REST Routers
app.include_router(weather_router, prefix="/api")
app.include_router(pest_router, prefix="/api")
app.include_router(irrigation_router, prefix="/api")
app.include_router(crops_router, prefix="/api")
app.include_router(treatment_router, prefix="/api")
app.include_router(disease_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(settings_router, prefix="/api")

@app.get("/api/info")
def system_info():
    return {
        "project": "KRISHIRAKSHAK",
        "title": "AI-Based Weather-Driven Pest Forecasting, Smart Irrigation, and Crop Recommendation System",
        "tagline": "Predict. Detect. Irrigate. Protect.",
        "version": settings.VERSION,
        "mode": settings.DATA_MODE,
        "mode_badge": "DATASET MODE" if settings.DATA_MODE == "dataset" else "LIVE WEATHER MODE",
        "docs_url": "/docs",
        "disease_detection_status": "ON HOLD (EfficientNet-B0 integration placeholder active)",
        "hardware_status": "Dataset-based soil moisture active (ESP32 LiveSensorProvider ready)"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "KrishiRakshak Decision Engine",
        "data_mode": settings.DATA_MODE
    }

# Mount Frontend Static SPA
from fastapi.staticfiles import StaticFiles
frontend_dir = os.path.join(project_root, "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
