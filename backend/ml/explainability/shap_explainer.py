"""
SHAP Explainability Module for KrishiRakshak
Uses TreeSHAP to compute exact additive feature attributions for pest risk forecasts.
"""
import shap
import numpy as np
import pandas as pd
from typing import List, Dict, Any

class PestShapExplainer:
    """Computes and formats TreeSHAP explanations for pest predictions."""
    def __init__(self, model, feature_names: List[str], class_names: List[str]):
        self.model = model
        self.feature_names = feature_names
        self.class_names = class_names
        self.explainer = shap.TreeExplainer(model)

    def explain_instance(self, X_input: pd.DataFrame, predicted_class_idx: int) -> List[Dict[str, Any]]:
        """
        Calculates SHAP values for the specified input instance and target predicted class.
        Returns sorted feature contributions with human-understandable explanations.
        """
        shap_values = self.explainer.shap_values(X_input)
        
        # In multiclass XGBoost, TreeSHAP returns an array of shape (n_samples, n_features, n_classes)
        # or list of arrays per class. Let's handle both representations.
        if isinstance(shap_values, list):
            class_shap = shap_values[predicted_class_idx][0]
        elif len(shap_values.shape) == 3:
            class_shap = shap_values[0, :, predicted_class_idx]
        else:
            class_shap = shap_values[0]

        contributions = []
        feature_labels = {
            'temperature': 'Temperature (°C)',
            'humidity': 'Relative Humidity (%)',
            'rainfall': 'Rainfall (mm)',
            'N': 'Soil Nitrogen Level',
            'P': 'Phosphorus Level',
            'K': 'Potassium Level',
            'ph': 'Soil pH',
            'crop_encoded': 'Crop Host Vulnerability'
        }

        feature_advice = {
            'temperature': {
                'pos': 'Elevated warm temperature accelerates insect reproduction and egg hatching.',
                'neg': 'Sub-optimal temperature restricts insect metabolic growth.'
            },
            'humidity': {
                'pos': 'High humidity provides ideal conditions for soft-bodied pests and fungal spore germination.',
                'neg': 'Dry atmosphere inhibits pest oviposition and nymph survival.'
            },
            'rainfall': {
                'pos': 'Recent rainfall elevates foliage wetness and microclimate moisture.',
                'neg': 'Absence of precipitation lowers leaf surface humidity.'
            },
            'N': {
                'pos': 'Excess nitrogen promotes lush, tender succulent foliage attractive to sap-feeders.',
                'neg': 'Balanced nitrogen preserves natural plant epidermal toughness.'
            },
            'P': {
                'pos': 'Nutrient balance influences overall canopy microclimate.',
                'neg': 'Slight negative association with pest pressure.'
            },
            'K': {
                'pos': 'Potassium dynamics play a role in plant stress regulation.',
                'neg': 'Optimal potassium enhances crop mechanical tissue defense.'
            },
            'ph': {
                'pos': 'Soil pH impacts micronutrient uptake and host tolerance.',
                'neg': 'Stable soil pH maintains standard crop defense.'
            },
            'crop_encoded': {
                'pos': 'Target crop variety has documented susceptibility to seasonal pest vectors.',
                'neg': 'Target crop demonstrates baseline tolerance to this microclimate.'
            }
        }

        for idx, feat in enumerate(self.feature_names):
            val = float(class_shap[idx])
            raw_input_val = float(X_input.iloc[0][feat])
            human_feat = feature_labels.get(feat, feat)
            
            is_positive = val > 0
            reason = feature_advice.get(feat, {}).get('pos' if is_positive else 'neg', '')

            contributions.append({
                'feature': feat,
                'label': human_feat,
                'input_value': round(raw_input_val, 2),
                'shap_value': round(val, 4),
                'impact': 'increases_risk' if is_positive else 'decreases_risk',
                'contribution_sign': '+' if is_positive else '-',
                'description': f"{human_feat} ({raw_input_val:.1f}): {'+' if is_positive else ''}{val:+.3f} contribution",
                'reasoning': reason
            })

        # Sort by absolute contribution strength (highest impact first)
        contributions.sort(key=lambda x: abs(x['shap_value']), reverse=True)
        return contributions
