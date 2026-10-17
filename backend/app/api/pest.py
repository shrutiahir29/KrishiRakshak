"""
Pest Risk Forecasting API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.app.core.database import get_db
from backend.app.schemas.pest import PestPredictRequest, PestPredictResponse
from backend.app.services.pest_service import pest_service
from backend.app.models.models import PestPrediction

router = APIRouter(prefix="/pest", tags=["Pest Forecasting"])

@router.post("/predict", response_model=PestPredictResponse)
def predict_pest_risk(payload: PestPredictRequest, db: Session = Depends(get_db)):
    """
    Predicts pest risk 3-5 days in advance using trained XGBoost Classifier
    and generates exact TreeSHAP feature attributions.
    """
    try:
        result = pest_service.predict(
            temperature=payload.temperature,
            humidity=payload.humidity,
            rainfall=payload.rainfall,
            crop=payload.crop,
            N=payload.N,
            P=payload.P,
            K=payload.K,
            ph=payload.ph
        )

        # Record in historical database
        try:
            record = PestPrediction(
                crop=payload.crop,
                predicted_risk=result["predicted_risk"],
                probability=result["probability"],
                forecast_days=result["forecast_window"],
                input_features=result["input_features"],
                shap_explanations=result["shap_explanations"],
                model_version=result["model_version"]
            )
            db.add(record)
            db.commit()
        except Exception:
            db.rollback()

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pest inference error: {str(e)}")

@router.get("/metrics")
def get_model_metrics() -> Dict[str, Any]:
    """Returns training metrics, accuracy, F1 score, and confusion matrix."""
    return pest_service.get_metrics()

@router.get("/history")
def get_pest_prediction_history(limit: int = 15, db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Retrieves recent pest prediction records from database."""
    try:
        records = db.query(PestPrediction).order_by(PestPrediction.id.desc()).limit(limit).all()
        return [
            {
                "id": r.id,
                "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.timestamp else "",
                "crop": r.crop,
                "predicted_risk": r.predicted_risk,
                "probability": r.probability,
                "probability_percent": round(r.probability * 100, 1),
                "features": r.input_features,
                "shap_explanations": r.shap_explanations
            }
            for r in records
        ]
    except Exception:
        return []
