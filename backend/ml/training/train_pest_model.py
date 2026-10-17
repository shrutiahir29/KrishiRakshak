"""
Training Pipeline for KrishiRakshak Pest Risk Forecasting Model
Trains an XGBoost Classifier and computes model metrics & artifacts.
"""
import os
import sys
import json
import joblib
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import xgboost as xgb

# Ensure backend root is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, "../../.."))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from backend.ml.preprocessing.preprocessor import PestDataPreprocessor, FEATURE_COLUMNS

def train_pest_model(
    data_path: str = None,
    output_dir: str = None
):
    print("=" * 60)
    print("KRISHIRAKSHAK — PEST RISK FORECASTING MODEL TRAINING")
    print("=" * 60)

    if data_path is None:
        # Check both potential dataset paths
        cand1 = os.path.join(backend_root, "data/raw/Crop_recommendation.csv")
        cand2 = os.path.join(backend_root, "Crop_recommendation.csv")
        data_path = cand1 if os.path.exists(cand1) else cand2

    if output_dir is None:
        output_dir = os.path.join(backend_root, "backend/ml/models")

    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading dataset from: {data_path}")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")

    # 1. Preprocessing
    preprocessor = PestDataPreprocessor()
    X, y, df_processed = preprocessor.prepare_training_data(data_path)

    print(f"Dataset shape: {df_processed.shape}")
    print(f"Features: {FEATURE_COLUMNS}")
    print("Target class distribution:")
    class_counts = df_processed['pest_risk'].value_counts().to_dict()
    for cls, cnt in class_counts.items():
        print(f"  - {cls}: {cnt} samples ({cnt/len(df_processed)*100:.1f}%)")

    # 2. Stratified Train / Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Train split: {len(X_train)} samples, Test split: {len(X_test)} samples")

    # 3. XGBoost Classifier
    print("\nTraining XGBoost Classifier...")
    clf = xgb.XGBClassifier(
        n_estimators=150,
        max_depth=5,
        learning_rate=0.08,
        subsample=0.85,
        colsample_bytree=0.85,
        objective="multi:softprob",
        eval_metric="mlogloss",
        random_state=42
    )
    clf.fit(X_train, y_train)

    # 4. Evaluation
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)

    acc = float(accuracy_score(y_test, y_pred))
    prec_macro = float(precision_score(y_test, y_pred, average="macro"))
    prec_weighted = float(precision_score(y_test, y_pred, average="weighted"))
    rec_macro = float(recall_score(y_test, y_pred, average="macro"))
    rec_weighted = float(recall_score(y_test, y_pred, average="weighted"))
    f1_macro = float(f1_score(y_test, y_pred, average="macro"))
    f1_weighted = float(f1_score(y_test, y_pred, average="weighted"))
    cm = confusion_matrix(y_test, y_pred).tolist()

    class_names = preprocessor.target_encoder.classes_.tolist()
    print("\nEvaluation Results:")
    print(f"Accuracy:          {acc:.4f} ({acc*100:.2f}%)")
    print(f"Macro F1:          {f1_macro:.4f}")
    print(f"Weighted F1:       {f1_weighted:.4f}")
    print(f"Macro Precision:   {prec_macro:.4f}")
    print(f"Macro Recall:      {rec_macro:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=class_names))

    # 5. Save Artifacts
    model_path = os.path.join(output_dir, "pest_xgboost.pkl")
    preproc_path = os.path.join(output_dir, "pest_preprocessor.pkl")
    metrics_path = os.path.join(output_dir, "model_metrics.json")

    joblib.dump(clf, model_path)
    preprocessor.save(preproc_path)

    metrics = {
        "model_name": "XGBoost Classifier (Pest Risk 3-5 Days Ahead)",
        "model_type": "xgboost.XGBClassifier",
        "training_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dataset_used": os.path.basename(data_path),
        "total_records": len(df_processed),
        "training_samples": len(X_train),
        "testing_samples": len(X_test),
        "feature_names": FEATURE_COLUMNS,
        "target_classes": class_names,
        "class_distribution": class_counts,
        "metrics": {
            "accuracy": round(acc, 4),
            "macro_precision": round(prec_macro, 4),
            "weighted_precision": round(prec_weighted, 4),
            "macro_recall": round(rec_macro, 4),
            "weighted_recall": round(rec_weighted, 4),
            "macro_f1": round(f1_macro, 4),
            "weighted_f1": round(f1_weighted, 4),
            "confusion_matrix": cm
        },
        "explainability": "TreeSHAP (Tree-based Shapley Additive exPlanations)",
        "forecast_window": "3-5 days in advance"
    }

    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    print("\nArtifacts saved successfully:")
    print(f" - Model: {model_path}")
    print(f" - Preprocessor: {preproc_path}")
    print(f" - Metrics: {metrics_path}")
    print("=" * 60)
    return metrics

if __name__ == "__main__":
    train_pest_model()
