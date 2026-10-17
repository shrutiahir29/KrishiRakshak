"""
Pest Risk Prediction Service for KrishiRakshak
Loads the trained XGBoost model, runs inference, and computes TreeSHAP explanations.
"""
import os
import json
import joblib
from datetime import datetime
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from backend.app.core.config import settings
from backend.ml.preprocessing.preprocessor import PestDataPreprocessor, FEATURE_COLUMNS
from backend.ml.explainability.shap_explainer import PestShapExplainer
from backend.ml.training.train_pest_model import train_pest_model

class PestRiskService:
    """Manages model lifecycle, predictions, and TreeSHAP explainability."""

    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.metrics = None
        self.shap_explainer = None
        self._ensure_loaded()

    def _ensure_loaded(self):
        """Loads model artifacts or triggers training pipeline if missing."""
        model_path = os.path.join(settings.MODELS_DIR, "pest_xgboost.pkl")
        preproc_path = os.path.join(settings.MODELS_DIR, "pest_preprocessor.pkl")
        metrics_path = os.path.join(settings.MODELS_DIR, "model_metrics.json")

        if not (os.path.exists(model_path) and os.path.exists(preproc_path)):
            print("Model artifacts not found. Initiating automated training pipeline...")
            train_pest_model()

        self.model = joblib.load(model_path)
        self.preprocessor = PestDataPreprocessor.load(preproc_path)

        if os.path.exists(metrics_path):
            with open(metrics_path, "r") as f:
                self.metrics = json.load(f)
        else:
            self.metrics = {}

        class_names = self.preprocessor.target_encoder.classes_.tolist()
        self.shap_explainer = PestShapExplainer(
            model=self.model,
            feature_names=FEATURE_COLUMNS,
            class_names=class_names
        )

    def get_metrics(self) -> Dict[str, Any]:
        """Returns model evaluation metrics."""
        return self.metrics

    def predict(
        self,
        temperature: float,
        humidity: float,
        rainfall: float,
        crop: str = "cotton",
        N: float = 60.0,
        P: float = 40.0,
        K: float = 40.0,
        ph: float = 6.5
    ) -> Dict[str, Any]:
        """
        Executes real XGBoost inference and TreeSHAP attribution.
        Outputs exact predictions and additive feature contributions.
        """
        self._ensure_loaded()

        # Transform single input instance
        X_input = self.preprocessor.transform_single_input(
            temperature=temperature,
            humidity=humidity,
            rainfall=rainfall,
            crop=crop,
            N=N,
            P=P,
            K=K,
            ph=ph
        )

        # Model prediction
        pred_idx = int(self.model.predict(X_input)[0])
        probabilities = self.model.predict_proba(X_input)[0]
        confidence = float(probabilities[pred_idx])

        class_names = self.preprocessor.target_encoder.classes_.tolist()
        predicted_risk = class_names[pred_idx] # LOW, MEDIUM, or HIGH

        # Compute TreeSHAP explanations
        shap_contributions = self.shap_explainer.explain_instance(X_input, pred_idx)

        # Highlight top 3 decisive factors for the farmer
        top_factors = [
            f"{c['label']}: {'+' if c['shap_value'] > 0 else ''}{c['shap_value']:.2f} contribution"
            for c in shap_contributions[:3]
        ]

        # Actionable IPM advice based on predicted risk
        if predicted_risk == "HIGH":
            action_summary = "High pest risk anticipated over next 3-5 days. Inspect crop foliage for egg clusters and early nymph stages. Prepare IPM bio-pesticides or pheromone traps."
        elif predicted_risk == "MEDIUM":
            action_summary = "Moderate microclimate favorability. Monitor weekly trap counts; maintain balanced canopy aeration."
        else:
            action_summary = "Pest risk is low. Environmental conditions do not favor significant pest outbreaks. Continue standard monitoring."

        return {
            "predicted_risk": predicted_risk,
            "probability": round(confidence, 4),
            "probability_percent": round(confidence * 100, 1),
            "forecast_window": "3-5 days ahead",
            "crop": crop,
            "input_features": {
                "temperature": temperature,
                "humidity": humidity,
                "rainfall": rainfall,
                "N": N,
                "P": P,
                "K": K,
                "ph": ph
            },
            "class_probabilities": {
                class_names[i]: round(float(probabilities[i]) * 100, 1)
                for i in range(len(class_names))
            },
            "shap_explanations": shap_contributions,
            "top_drivers": top_factors,
            "action_summary": action_summary,
            "model_version": "XGBoost-TreeSHAP-1.0",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

pest_service = PestRiskService()
