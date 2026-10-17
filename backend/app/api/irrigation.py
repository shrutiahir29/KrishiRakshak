"""
Smart Irrigation API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.app.core.database import get_db
from backend.app.schemas.irrigation import (
    IrrigationCurrentResponse, IrrigationAdvisoryRequest, IrrigationAdvisoryResponse
)
from backend.app.services.irrigation_service import irrigation_engine, dataset_provider
from backend.app.models.models import IrrigationAdvisory

router = APIRouter(prefix="/irrigation", tags=["Smart Irrigation"])

@router.get("/current", response_model=IrrigationCurrentResponse)
def get_current_soil_moisture():
    """
    Retrieves latest soil moisture observation via SoilMoistureDataProvider abstraction.
    Truthfulness rule: Returns 'Dataset-Based Soil Moisture'.
    """
    return dataset_provider.get_latest_reading()

@router.post("/advisory", response_model=IrrigationAdvisoryResponse)
def generate_irrigation_advisory(payload: IrrigationAdvisoryRequest, db: Session = Depends(get_db)):
    """
    Computes smart irrigation recommendation combining soil moisture,
    FAO-56 ETc, and rainfall forecast.
    """
    try:
        advisory = irrigation_engine.generate_advisory(
            crop=payload.crop,
            growth_stage=payload.growth_stage,
            soil_type=payload.soil_type,
            irrigation_method=payload.irrigation_method,
            forecast_rain_48h=payload.forecast_rain_48h,
            manual_soil_moisture=payload.manual_soil_moisture
        )

        # Store in historical database
        try:
            record = IrrigationAdvisory(
                crop=payload.crop,
                soil_moisture_vwc=advisory["soil_moisture_vwc"],
                field_capacity=advisory["field_capacity_percent"] / 100.0,
                wilting_point=advisory["wilting_point_percent"] / 100.0,
                eto=advisory["eto_mm_day"],
                etc=advisory["etc_mm_day"],
                forecast_rain_48h=advisory["forecast_rain_48h"],
                decision=advisory["decision"],
                intensity=advisory["intensity"],
                water_amount_mm=advisory["water_amount_mm"],
                reasoning="; ".join(advisory["reasons"]),
                data_source=advisory["data_source"]
            )
            db.add(record)
            db.commit()
        except Exception:
            db.rollback()

        return advisory
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Irrigation calculation error: {str(e)}")

@router.get("/history")
def get_irrigation_history(limit: int = 15, db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Retrieves recent irrigation advisories."""
    try:
        records = db.query(IrrigationAdvisory).order_by(IrrigationAdvisory.id.desc()).limit(limit).all()
        return [
            {
                "id": r.id,
                "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.timestamp else "",
                "crop": r.crop,
                "soil_moisture_percent": round(r.soil_moisture_vwc * 100, 1),
                "decision": r.decision,
                "intensity": r.intensity,
                "water_amount_mm": r.water_amount_mm,
                "reasoning": r.reasoning
            }
            for r in records
        ]
    except Exception:
        return []
