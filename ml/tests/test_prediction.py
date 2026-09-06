"""
Standalone inference test suite for the landslide risk ML model.
"""

import sys
import warnings
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "ml"))

import joblib
import numpy as np
from FEATURES import FEATURE_NAMES, IMPUTER_MEDIANS, RISK_THRESHOLDS

warnings.filterwarnings("ignore", category=UserWarning)

MODEL_PATH = PROJECT_ROOT / "ml/models/final_landslide_risk_model.joblib"


def load_model():
    assert MODEL_PATH.exists(), f"Model file not found: {MODEL_PATH}"
    model = joblib.load(MODEL_PATH)
    assert hasattr(model, "predict_proba"), "Model does not implement predict_proba"
    return model


def predict(model, **kwargs):
    row = [kwargs.get(f, np.nan) for f in FEATURE_NAMES]
    X = np.array([row], dtype=float)
    proba = model.predict_proba(X)[0]
    p_landslide = float(proba[1])
    for label, thresh in [("CRITICAL", 0.75), ("HIGH", 0.55), ("MEDIUM", 0.35), ("LOW", 0.0)]:
        if p_landslide >= thresh:
            risk = label
            break
    return p_landslide, risk


def test_1_known_landslide_sample(model):
    """Event 141 (Meghalaya) — heavy rain 86mm 1d, 426mm 7d, slope 31.7°"""
    p, risk = predict(
        model,
        rainfall_1d=86.06,
        rainfall_3d=394.86,
        rainfall_7d=426.40,
        elevation_m=1300.39,
        slope_degrees=31.74,
        soil_moisture=0.394,
    )
    print(f"Test 1 (Heavy rain/slope landslide): p={p:.4f}, risk={risk}")
    assert p >= 0.50, f"Expected high probability, got {p}"
    print("  [PASS]")


def test_2_known_background_sample(model):
    """Low rain, flat terrain"""
    p, risk = predict(
        model,
        rainfall_1d=0.0,
        rainfall_3d=0.0,
        rainfall_7d=2.0,
        elevation_m=200.0,
        slope_degrees=2.0,
        soil_moisture=0.20,
    )
    print(f"Test 2 (Dry/flat background): p={p:.4f}, risk={risk}")
    assert p <= 0.40, f"Expected low probability, got {p}"
    print("  [PASS]")


def test_3_determinism(model):
    """Same input must give identical output"""
    inputs = dict(
        rainfall_1d=25.0,
        rainfall_3d=80.0,
        rainfall_7d=150.0,
        elevation_m=900.0,
        slope_degrees=20.0,
        soil_moisture=0.35,
    )
    p1, _ = predict(model, **inputs)
    p2, _ = predict(model, **inputs)
    assert p1 == p2, f"Predictions differ: {p1} != {p2}"
    print(f"Test 3 (Determinism): p1={p1} == p2={p2}")
    print("  [PASS]")


def test_4_all_missing_values(model):
    """All NaN should not crash — imputer fills with medians"""
    p, risk = predict(model)
    print(f"Test 4 (All NaN input): p={p:.4f}, risk={risk}")
    assert 0.0 <= p <= 1.0, f"Probability out of range: {p}"
    print("  [PASS]")


def test_5_extreme_values(model):
    """High rainfall in steep terrain (realistic extreme event)"""
    p, risk = predict(
        model,
        rainfall_1d=120.0,
        rainfall_3d=350.0,
        rainfall_7d=600.0,
        elevation_m=1200.0,
        slope_degrees=42.0,
        soil_moisture=0.45,
    )
    print(f"Test 5 (Extreme realistic event): p={p:.4f}, risk={risk}")
    assert p >= 0.55, f"Expected HIGH/CRITICAL (>=0.55), got {p}"
    assert risk in ("HIGH", "CRITICAL"), f"Expected HIGH or CRITICAL risk, got {risk}"
    print("  [PASS]")


def test_6_pipeline_imputer_medians(model):
    """Verify that the pipeline imputer matches ml/FEATURES.py"""
    imp = model.named_steps["imputer"]
    print("Test 6 (Imputer medians match FEATURES.py):")
    for i, name in enumerate(FEATURE_NAMES):
        expected = IMPUTER_MEDIANS[name]
        actual = imp.statistics_[i]
        diff = abs(actual - expected)
        print(f"  {name:15s}: expected={expected:8.2f}, actual={actual:8.2f}")
        assert diff < 0.1, f"Median mismatch for {name}: {actual} vs {expected}"
    print("  [PASS]")


def run_all_tests():
    print("=" * 60)
    print("RUNNING INFERENCE TESTS")
    print("=" * 60)

    model = load_model()
    print("Model loaded successfully.\n")

    test_1_known_landslide_sample(model)
    test_2_known_background_sample(model)
    test_3_determinism(model)
    test_4_all_missing_values(model)
    test_5_extreme_values(model)
    test_6_pipeline_imputer_medians(model)

    print("\n" + "=" * 60)
    print("ALL 6 INFERENCE TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
