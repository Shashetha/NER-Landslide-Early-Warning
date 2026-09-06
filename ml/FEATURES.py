"""
Single source of truth for the final landslide risk model feature contract.

Training dataset: data/processed/final_ml_dataset.csv
Model file:       ml/models/final_landslide_risk_model.joblib

CRITICAL — feature order must be IDENTICAL to training order.
Do NOT reorder these without retraining the model.
"""

FEATURE_NAMES = [
    "rainfall_1d",
    "rainfall_3d",
    "rainfall_7d",
    "elevation_m",
    "slope_degrees",
    "soil_moisture",
]

FEATURE_UNITS = {
    "rainfall_1d":    "mm   — 1-day cumulative rainfall",
    "rainfall_3d":    "mm   — 3-day cumulative rainfall",
    "rainfall_7d":    "mm   — 7-day cumulative rainfall",
    "elevation_m":    "m    — elevation above sea level",
    "slope_degrees":  "°    — terrain slope angle",
    "soil_moisture":  "fraction 0–1 (e.g. 0.35 = 35% volumetric)",
}

FEATURE_TRAINING_RANGES = {
    "rainfall_1d":   (0.0,    519.6),
    "rainfall_3d":   (0.0,   1194.1),
    "rainfall_7d":   (0.0,   2073.9),
    "elevation_m":   (10.0,  4200.0),
    "slope_degrees": (0.0,     66.0),
    "soil_moisture": (0.16,    0.57),
}

IMPUTER_MEDIANS = {
    "rainfall_1d":   5.89,
    "rainfall_3d":   33.26,
    "rainfall_7d":   102.52,
    "elevation_m":   856.38,
    "slope_degrees": 12.65,
    "soil_moisture": 0.3418,
}

SOIL_MOISTURE_SCALE = "fraction"
"""
soil_moisture MUST be in the range 0–1 (volumetric fraction).
The training data was extracted from NASA SMAP (m³/m³).
If an external provider returns percentages (0–100), divide by 100 before inference.
"""

MODEL_CLASSES = [0, 1]
"""0 = no landslide (background), 1 = landslide"""

RISK_THRESHOLDS = {
    "CRITICAL": 0.75,
    "HIGH":     0.55,
    "MEDIUM":   0.35,
    "LOW":      0.0,
}
"""
Probability → risk level mapping.
Thresholds are based on equal-split balanced dataset (351 positive / 351 background).
For deployment: consider lowering CRITICAL/HIGH thresholds to reduce false negatives.
"""
