"""
Crop Recommendation API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Dict, Any
from backend.app.core.database import get_db
from backend.app.schemas.crops import CropRecommendRequest, CropRecommendResponse
from backend.app.core.crop_rules import calculate_crop_suitability, CROP_RULES
from backend.app.models.models import CropRecommendation

router = APIRouter(prefix="/crops", tags=["Crop Recommendation"])

@router.post("/recommend", response_model=CropRecommendResponse)
def recommend_crops(payload: CropRecommendRequest, db: Session = Depends(get_db)):
    """
    Evaluates rule-based agronomic suitability scoring using dataset-derived rules.
    Returns ranked crop recommendations with transparent reasons and sub-scores.
    """
    try:
        recommendations = calculate_crop_suitability(
            n=payload.N,
            p=payload.P,
            k=payload.K,
            temperature=payload.temperature,
            humidity=payload.humidity,
            ph=payload.ph,
            rainfall=payload.rainfall,
            top_k=payload.top_k
        )

        input_data = {
            "N": payload.N,
            "P": payload.P,
            "K": payload.K,
            "temperature": payload.temperature,
            "humidity": payload.humidity,
            "ph": payload.ph,
            "rainfall": payload.rainfall
        }

        # Save to database
        try:
            rec_record = CropRecommendation(
                n_input=payload.N,
                p_input=payload.P,
                k_input=payload.K,
                temperature=payload.temperature,
                humidity=payload.humidity,
                ph=payload.ph,
                rainfall=payload.rainfall,
                recommendations=recommendations
            )
            db.add(rec_record)
            db.commit()
        except Exception:
            db.rollback()

        return {
            "method": "Rule-Based Agronomic Suitability Scoring",
            "total_evaluated": len(CROP_RULES),
            "recommendations": recommendations,
            "input_conditions": input_data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crop recommendation error: {str(e)}")

@router.get("/rules")
def get_configured_crop_rules() -> Dict[str, Any]:
    """Returns the configurable agronomic envelope rules for all crops."""
    return CROP_RULES

@router.get("/history")
def get_recommendation_history(limit: int = 15, db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Retrieves previous recommendation queries."""
    try:
        records = db.query(CropRecommendation).order_by(CropRecommendation.id.desc()).limit(limit).all()
        return [
            {
                "id": r.id,
                "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.timestamp else "",
                "inputs": {
                    "N": r.n_input, "P": r.p_input, "K": r.k_input,
                    "temperature": r.temperature, "humidity": r.humidity,
                    "ph": r.ph, "rainfall": r.rainfall
                },
                "recommendations": r.recommendations
            }
            for r in records
        ]
    except Exception:
        return []
