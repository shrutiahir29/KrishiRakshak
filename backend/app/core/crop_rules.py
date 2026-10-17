"""
Configurable Crop Requirement Rules & Agronomic Suitability Engine for KrishiRakshak
Pure rule-based scoring system derived directly from the project dataset.
"""
import os
import json
from typing import Dict, Any, List

RULES_FILE = os.path.join(os.path.dirname(__file__), "crop_rules_data.json")

def load_crop_rules() -> Dict[str, Any]:
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r") as f:
            return json.load(f)
    return {}

CROP_RULES = load_crop_rules()

def evaluate_parameter_score(val: float, bounds: Dict[str, float]) -> float:
    """
    Computes a continuous suitability score between 0.0 and 1.0 using trapezoidal membership.
    If within opt_min and opt_max -> 1.0 (100% suitable)
    If between min and opt_min -> linear ramp up
    If between opt_max and max -> linear ramp down
    Outside min/max -> smoothly penalties
    """
    vmin = bounds['min']
    vopt_min = bounds['opt_min']
    vopt_max = bounds['opt_max']
    vmax = bounds['max']

    if vopt_min <= val <= vopt_max:
        return 1.0
    elif vmin <= val < vopt_min:
        return max(0.2, (val - vmin) / max(0.01, vopt_min - vmin))
    elif vopt_max < val <= vmax:
        return max(0.2, (vmax - val) / max(0.01, vmax - vopt_max))
    else:
        # Distance penalty
        if val < vmin:
            dist = vmin - val
            margin = max(1.0, vopt_min - vmin)
            return max(0.0, 0.2 - (dist / margin) * 0.2)
        else:
            dist = val - vmax
            margin = max(1.0, vmax - vopt_max)
            return max(0.0, 0.2 - (dist / margin) * 0.2)

def calculate_crop_suitability(
    n: float, p: float, k: float,
    temperature: float, humidity: float, ph: float, rainfall: float,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Evaluates rule-based suitability for all configured crops and generates
    detailed transparent explanations for why each crop is recommended.
    """
    results = []

    # Agronomic weights
    weights = {
        'temperature': 0.22,
        'rainfall': 0.22,
        'humidity': 0.16,
        'ph': 0.15,
        'nutrients': 0.25 # N: 0.10, P: 0.08, K: 0.07
    }

    for crop_name, reqs in CROP_RULES.items():
        s_temp = evaluate_parameter_score(temperature, reqs['temperature'])
        s_rain = evaluate_parameter_score(rainfall, reqs['rainfall'])
        s_hum = evaluate_parameter_score(humidity, reqs['humidity'])
        s_ph = evaluate_parameter_score(ph, reqs['ph'])
        s_n = evaluate_parameter_score(n, reqs['N'])
        s_p = evaluate_parameter_score(p, reqs['P'])
        s_k = evaluate_parameter_score(k, reqs['K'])

        s_nutrients = (0.40 * s_n) + (0.32 * s_p) + (0.28 * s_k)

        composite_score = (
            weights['temperature'] * s_temp +
            weights['rainfall'] * s_rain +
            weights['humidity'] * s_hum +
            weights['ph'] * s_ph +
            weights['nutrients'] * s_nutrients
        )
        score_percent = round(composite_score * 100.0, 1)

        # Transparent reasoning explanations
        reasons = []
        if s_temp >= 0.8:
            reasons.append(f"+ Suitable temperature ({temperature:.1f}°C matches required {reqs['temperature']['min']:.0f}–{reqs['temperature']['max']:.0f}°C)")
        elif s_temp < 0.4:
            reasons.append(f"- Sub-optimal temperature ({temperature:.1f}°C vs ideal {reqs['temperature']['opt_min']:.0f}–{reqs['temperature']['opt_max']:.0f}°C)")

        if s_rain >= 0.8:
            reasons.append(f"+ Suitable rainfall ({rainfall:.0f} mm matches water regime)")
        elif s_rain < 0.4:
            reasons.append(f"- Water stress / rainfall deficit ({rainfall:.0f} mm vs needed {reqs['rainfall']['opt_min']:.0f}–{reqs['rainfall']['opt_max']:.0f} mm)")

        if s_ph >= 0.8:
            reasons.append(f"+ Suitable soil pH ({ph:.1f} within tolerance {reqs['ph']['min']:.1f}–{reqs['ph']['max']:.1f})")
        elif s_ph < 0.4:
            reasons.append(f"- Incompatible pH ({ph:.1f} outside preferred {reqs['ph']['opt_min']:.1f}–{reqs['ph']['opt_max']:.1f})")

        if s_nutrients >= 0.8:
            reasons.append(f"+ Favorable N-P-K nutrient profile (N:{n:.0f}, P:{p:.0f}, K:{k:.0f})")
        elif s_nutrients < 0.4:
            reasons.append(f"- Nutrient imbalance for high-demand crop")

        if s_hum >= 0.8:
            reasons.append(f"+ Compatible atmospheric humidity ({humidity:.1f}%)")

        results.append({
            'crop': crop_name.capitalize(),
            'crop_code': crop_name,
            'score': score_percent,
            'sub_scores': {
                'temperature': round(s_temp * 100, 1),
                'rainfall': round(s_rain * 100, 1),
                'humidity': round(s_hum * 100, 1),
                'ph': round(s_ph * 100, 1),
                'nutrients': round(s_nutrients * 100, 1)
            },
            'reasons': reasons,
            'optimal_conditions': {
                'temp_range': f"{reqs['temperature']['opt_min']} - {reqs['temperature']['opt_max']} °C",
                'rain_range': f"{reqs['rainfall']['opt_min']} - {reqs['rainfall']['opt_max']} mm",
                'ph_range': f"{reqs['ph']['opt_min']} - {reqs['ph']['opt_max']}"
            }
        })

    # Sort descending by score
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]
