import os
import sys
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_FILE = BASE_DIR / "data/processed/final_ml_dataset.csv"
MODEL_FILE = BASE_DIR / "ml/models/final_landslide_risk_model.joblib"
METRICS_FILE = BASE_DIR / "ml/models/model_metrics.json"

import json
import joblib
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

print("=" * 65)
print("TRAINING LANDSLIDE RISK ML MODEL FROM REAL NER DATASET")
print("=" * 65)
print(f"Loading dataset: {DATA_FILE}")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    lines = [l.strip().split(",") for l in f if l.strip()]

header = lines[0]
rows = lines[1:]

features = [
    "rainfall_1d",
    "rainfall_3d",
    "rainfall_7d",
    "elevation_m",
    "slope_degrees",
    "soil_moisture"
]

idx_map = {name: header.index(name) for name in features + ["target", "latitude", "longitude", "state"]}

X_raw, y_raw, coords, states = [], [], [], []
for r in rows:
    feat = []
    for k in features:
        val = r[idx_map[k]]
        feat.append(float(val) if val != "" and val.lower() != "nan" else np.nan)
    X_raw.append(feat)
    y_raw.append(int(r[idx_map["target"]]))
    coords.append((float(r[idx_map["latitude"]]), float(r[idx_map["longitude"]])))
    states.append(r[idx_map["state"]])

X = np.array(X_raw, dtype=float)
y = np.array(y_raw, dtype=int)

print(f"Total Dataset Samples: {len(y)} (Landslide: {np.sum(y==1)}, Background: {np.sum(y==0)})")
print(f"Features: {', '.join(features)}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"\nTraining set: {len(y_train)} samples | Testing set: {len(y_test)} samples")

model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("classifier", RandomForestClassifier(
        n_estimators=250,
        max_depth=12,
        min_samples_split=4,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ))
])

print("\nFitting Random Forest Pipeline on training features...")
model.fit(X_train, y_train)
print("[OK] Model fitted successfully")

# Evaluation
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_proba)
cm = confusion_matrix(y_test, y_pred)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X, y, cv=cv, scoring="roc_auc")

print("\n" + "=" * 65)
print("EVALUATION METRICS ON UNSEEN TEST SAMPLES")
print("=" * 65)
print(f"Accuracy : {acc * 100:.2f}%")
print(f"Precision: {prec * 100:.2f}%")
print(f"Recall   : {rec * 100:.2f}% (Safety Critical: minimizes missed landslides)")
print(f"F1-Score : {f1 * 100:.2f}%")
print(f"ROC-AUC  : {roc_auc:.4f}")
print(f"5-Fold Cross-Validation ROC-AUC: {np.mean(cv_scores):.4f} (+/- {np.std(cv_scores):.4f})")
print(f"\nConfusion Matrix:\n{cm}")

clf = model.named_steps["classifier"]
importances = clf.feature_importances_
sorted_idx = np.argsort(importances)[::-1]

print("\nFeature Importance Breakdown:")
for i in sorted_idx:
    print(f" - {features[i]:16s}: {importances[i] * 100:6.2f}%")

MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_FILE)
print(f"\n[OK] Exported trained model artifact: {MODEL_FILE}")

metrics_data = {
    "model_name": "landslide-rf-final",
    "version": "1.0.0",
    "features": features,
    "metrics": {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(roc_auc, 4),
        "cv_roc_auc_mean": round(float(np.mean(cv_scores)), 4),
    },
    "confusion_matrix": {
        "true_negatives": int(cm[0, 0]),
        "false_positives": int(cm[0, 1]),
        "false_negatives": int(cm[1, 0]),
        "true_positives": int(cm[1, 1]),
    },
    "feature_importances": {features[i]: round(float(importances[i]), 4) for i in sorted_idx}
}

with open(METRICS_FILE, "w", encoding="utf-8") as f:
    json.dump(metrics_data, f, indent=2)

print(f"[OK] Exported model metadata & metrics: {METRICS_FILE}")
print("=" * 65)
