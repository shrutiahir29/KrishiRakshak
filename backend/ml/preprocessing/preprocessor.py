"""
Pest Preprocessing Pipeline for KrishiRakshak
Handles dataset loading, validation, encoding, and feature scaling/transformation.
"""
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib

CROP_LIST = [
    'rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
    'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate',
    'banana', 'mango', 'grapes', 'watermelon', 'muskmelon',
    'apple', 'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee'
]

FEATURE_COLUMNS = ['temperature', 'humidity', 'rainfall', 'N', 'P', 'K', 'ph', 'crop_encoded']

class PestDataPreprocessor:
    """Preprocessor for pest risk prediction."""
    def __init__(self):
        self.crop_encoder = LabelEncoder()
        self.target_encoder = LabelEncoder()
        self.feature_columns = FEATURE_COLUMNS
        self.is_fitted = False

    def fit_encoders(self, crops=None, targets=None):
        if crops is None:
            crops = CROP_LIST
        self.crop_encoder.fit(crops)
        if targets is None:
            targets = ['LOW', 'MEDIUM', 'HIGH']
        self.target_encoder.fit(targets)
        self.is_fitted = True

    def calculate_ipm_risk_score(self, df: pd.DataFrame) -> pd.Series:
        """
        Agrometeorological Integrated Pest Management (IPM) composite risk scoring
        based on temperature, relative humidity, rainfall, and nitrogen vigor.
        """
        # Optimal temperature curve (Gaussian centered around 27°C, range 20-34°C)
        t_score = np.exp(-((df['temperature'] - 27.0)**2) / (2 * (7.0**2)))
        
        # Logistic humidity curve: RH > 70% significantly elevates pest multiplication
        h_score = 1.0 / (1.0 + np.exp(-(df['humidity'] - 70.0) / 7.0))
        
        # Rainfall saturation score (leaf wetness factor)
        r_score = np.clip(df['rainfall'] / 130.0, 0.0, 1.0)
        
        # Nitrogen tissue succulence factor (sap-sucking pest attractor)
        n_val = df['N'] if 'N' in df.columns else 60.0
        n_score = np.clip(n_val / 100.0, 0.0, 1.0)

        # Composite microclimate pest favorability index (0-100)
        composite_score = 100.0 * (
            0.35 * h_score +
            0.35 * t_score +
            0.18 * r_score +
            0.12 * n_score
        )
        return composite_score

    def assign_risk_classes(self, scores: pd.Series) -> pd.Series:
        """Assign LOW, MEDIUM, HIGH according to agrometeorological thresholds."""
        return pd.cut(
            scores,
            bins=[-np.inf, 40.0, 68.0, np.inf],
            labels=['LOW', 'MEDIUM', 'HIGH']
        ).astype(str)

    def prepare_training_data(self, data_path: str):
        """Loads and prepares features and target from dataset."""
        df = pd.read_csv(data_path)
        
        # Verify required columns
        required = ['temperature', 'humidity', 'rainfall', 'N', 'P', 'K', 'ph', 'label']
        for col in required:
            if col not in df.columns:
                raise ValueError(f"Required column '{col}' missing from {data_path}")

        scores = self.calculate_ipm_risk_score(df)
        df['pest_risk'] = self.assign_risk_classes(scores)

        self.fit_encoders(crops=df['label'].unique(), targets=['LOW', 'MEDIUM', 'HIGH'])
        df['crop_encoded'] = self.crop_encoder.transform(df['label'])

        X = df[self.feature_columns]
        y = self.target_encoder.transform(df['pest_risk'])
        return X, y, df

    def transform_single_input(self, temperature: float, humidity: float, rainfall: float,
                               crop: str, N: float = 60.0, P: float = 40.0, K: float = 40.0,
                               ph: float = 6.5) -> pd.DataFrame:
        """Transforms a single query record into model-ready features."""
        crop_clean = crop.lower().strip()
        if crop_clean in self.crop_encoder.classes_:
            c_enc = self.crop_encoder.transform([crop_clean])[0]
        else:
            # Fallback to nearest crop class
            c_enc = 0
            
        row = pd.DataFrame([{
            'temperature': float(temperature),
            'humidity': float(humidity),
            'rainfall': float(rainfall),
            'N': float(N),
            'P': float(P),
            'K': float(K),
            'ph': float(ph),
            'crop_encoded': int(c_enc)
        }])
        return row[self.feature_columns]

    def save(self, filepath: str):
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str):
        return joblib.load(filepath)
