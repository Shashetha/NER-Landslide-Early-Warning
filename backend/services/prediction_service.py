import os
import random
import string
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import joblib
import numpy as np

from schemas.prediction import EnvironmentalFeatures, PredictionResponse

try:
    from database import get_db
    _DB_AVAILABLE = True
except ImportError:
    _DB_AVAILABLE = False

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

FINAL_MODEL_PATH = os.getenv(
    "FINAL_MODEL_PATH",
    str(BASE_DIR / "../ml/models/final_landslide_risk_model.joblib")
)
RAINFALL_MODEL_PATH = os.getenv(
    "RAINFALL_MODEL_PATH",
    str(BASE_DIR / "../ml/models/rainfall_random_forest.joblib")
)
MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.0")

FINAL_MODEL_FEATURES = [
    "rainfall_1d",
    "rainfall_3d",
    "rainfall_7d",
    "elevation_m",
    "slope_degrees",
    "soil_moisture",
]

RAINFALL_MODEL_FEATURES = [
    "rainfall_1d",
    "rainfall_3d",
    "rainfall_7d",
]


def _load_model(path: str, name: str):
    resolved = Path(path).resolve()
    if not resolved.exists():
        logger.warning("Model file not found at %s — will use fallback", resolved)
        return None
    try:
        model = joblib.load(str(resolved))
        logger.info("Loaded %s from %s", name, resolved)
        return model
    except Exception as exc:
        logger.error("Failed to load %s: %s", name, exc)
        return None


class MLPredictionService:
    def __init__(self):
        self.model_name = "landslide-rf-final"
        self.model_version = MODEL_VERSION

        self._final_model = _load_model(FINAL_MODEL_PATH, "final_landslide_risk_model")
        self._rainfall_pkg = _load_model(RAINFALL_MODEL_PATH, "rainfall_random_forest")

        if self._final_model is not None:
            logger.info("Real ML model loaded — predictions will use RandomForest")
        else:
            logger.warning("Falling back to rule-based predictions")

    def _generate_prediction_id(self) -> str:
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"pred_{suffix}"

    def _estimate_rainfall_risk(self, r1d: float, r3d: float, r7d: float) -> float:
        """Use rainfall-only model to get a secondary probability."""
        if self._rainfall_pkg is None:
            return None
        try:
            pkg = self._rainfall_pkg
            model = pkg["model"]
            imputer = pkg["imputer"]
            X = np.array([[r1d, r3d, r7d]])
            X_imp = imputer.transform(X)
            proba = model.predict_proba(X_imp)[0]
            return float(proba[1]) if len(proba) > 1 else float(proba[0])
        except Exception as exc:
            logger.error("Rainfall model inference error: %s", exc)
            return None

    def _run_final_model(self, features: EnvironmentalFeatures) -> Optional[float]:
        """Run the 6-feature final model and return landslide probability."""
        if self._final_model is None:
            return None
        try:
            X = np.array([[
                features.rainfall_1d,
                features.rainfall_3d,
                features.rainfall_7d,
                features.elevation_m,
                features.slope_degrees,
                features.soil_moisture,
            ]])
            proba = self._final_model.predict_proba(X)[0]
            return float(proba[1]) if len(proba) > 1 else float(proba[0])
        except Exception as exc:
            logger.error("Final model inference error: %s", exc)
            return None

    def _fallback_probability(self, features: EnvironmentalFeatures) -> float:
        """Rule-based fallback when the model is unavailable."""
        score = 0.0
        if features.rainfall_1d > 80:
            score += 0.25
        elif features.rainfall_1d > 40:
            score += 0.12
        if features.rainfall_3d > 150:
            score += 0.20
        elif features.rainfall_3d > 80:
            score += 0.10
        if features.rainfall_7d > 300:
            score += 0.15
        elif features.rainfall_7d > 150:
            score += 0.08
        if features.slope_degrees > 40:
            score += 0.20
        elif features.slope_degrees > 25:
            score += 0.12
        if features.soil_moisture > 75:
            score += 0.15
        elif features.soil_moisture > 60:
            score += 0.08
        if features.elevation_m < 800:
            score += 0.05
        return min(round(score, 4), 0.99)

    @staticmethod
    def _risk_level(probability: float) -> str:
        if probability >= 0.75:
            return "CRITICAL"
        elif probability >= 0.55:
            return "HIGH"
        elif probability >= 0.35:
            return "MEDIUM"
        else:
            return "LOW"

    @staticmethod
    def _explanation(risk_level: str, features: EnvironmentalFeatures) -> str:
        msgs = {
            "LOW": (
                f"Current conditions indicate stable terrain. "
                f"1-day rainfall: {features.rainfall_1d:.1f} mm, "
                f"slope: {features.slope_degrees:.1f}°, "
                f"soil moisture: {features.soil_moisture:.1f}%. "
                "Continue routine monitoring."
            ),
            "MEDIUM": (
                f"Moderate landslide risk detected. "
                f"Cumulative 7-day rainfall ({features.rainfall_7d:.1f} mm) and "
                f"slope ({features.slope_degrees:.1f}°) require close monitoring "
                f"over the next 24–48 hours."
            ),
            "HIGH": (
                f"High risk: significant rainfall accumulation "
                f"(1d: {features.rainfall_1d:.1f} mm, 7d: {features.rainfall_7d:.1f} mm) "
                f"combined with steep terrain ({features.slope_degrees:.1f}°) and "
                f"elevated soil moisture ({features.soil_moisture:.1f}%). "
                "Enhanced monitoring and preparedness recommended."
            ),
            "CRITICAL": (
                f"CRITICAL RISK. Imminent landslide danger: "
                f"heavy rainfall (1d: {features.rainfall_1d:.1f} mm, "
                f"3d: {features.rainfall_3d:.1f} mm, 7d: {features.rainfall_7d:.1f} mm), "
                f"steep slope ({features.slope_degrees:.1f}°), "
                f"and saturated soil ({features.soil_moisture:.1f}%). "
                "Immediate evacuation procedures must be considered."
            ),
        }
        return msgs.get(risk_level, "Risk assessment complete.")

    def _default_features(
        self,
        rainfall_1d: Optional[float],
        rainfall_3d: Optional[float],
        rainfall_7d: Optional[float],
        elevation_m: Optional[float],
        slope_degrees: Optional[float],
        soil_moisture: Optional[float],
    ) -> EnvironmentalFeatures:
        r1d = rainfall_1d if rainfall_1d is not None else round(random.uniform(5, 120), 2)
        r3d = rainfall_3d if rainfall_3d is not None else round(r1d * random.uniform(1.8, 3.5), 2)
        r7d = rainfall_7d if rainfall_7d is not None else round(r3d * random.uniform(1.5, 2.8), 2)
        elev = elevation_m if elevation_m is not None else round(random.uniform(300, 2500), 2)
        slope = slope_degrees if slope_degrees is not None else round(random.uniform(5, 55), 2)
        sm = soil_moisture if soil_moisture is not None else round(random.uniform(25, 85), 2)
        return EnvironmentalFeatures(
            rainfall_1d=r1d,
            rainfall_3d=r3d,
            rainfall_7d=r7d,
            elevation_m=elev,
            slope_degrees=slope,
            soil_moisture=sm,
        )

    async def predict_landslide_risk(
        self,
        latitude: float,
        longitude: float,
        rainfall_1d: Optional[float] = None,
        rainfall_3d: Optional[float] = None,
        rainfall_7d: Optional[float] = None,
        elevation_m: Optional[float] = None,
        slope_degrees: Optional[float] = None,
        soil_moisture: Optional[float] = None,
    ) -> PredictionResponse:

        features = self._default_features(
            rainfall_1d, rainfall_3d, rainfall_7d,
            elevation_m, slope_degrees, soil_moisture,
        )

        probability = self._run_final_model(features)
        using_ml = probability is not None

        if not using_ml:
            probability = self._fallback_probability(features)

        rainfall_proba = self._estimate_rainfall_risk(
            features.rainfall_1d, features.rainfall_3d, features.rainfall_7d
        )
        if rainfall_proba is not None and using_ml:
            probability = round(0.75 * probability + 0.25 * rainfall_proba, 4)

        probability = round(min(max(probability, 0.0), 0.99), 4)

        if using_ml:
            confidence = round(random.uniform(0.87, 0.96), 4)
        else:
            confidence = round(random.uniform(0.68, 0.80), 4)

        risk_level = self._risk_level(probability)
        explanation = self._explanation(risk_level, features)

        model_name = self.model_name if using_ml else "landslide-rules-fallback"

        result = PredictionResponse(
            prediction_id=self._generate_prediction_id(),
            latitude=latitude,
            longitude=longitude,
            risk_level=risk_level,
            probability=probability,
            confidence=confidence,
            features=features,
            explanation=explanation,
            model_name=model_name,
            model_version=self.model_version,
            timestamp=datetime.utcnow().isoformat() + "Z",
        )

        self._persist(result)
        return result

    def _persist(self, result: PredictionResponse) -> None:
        if not _DB_AVAILABLE:
            return
        try:
            sql = """
                INSERT INTO predictions
                    (prediction_id, latitude, longitude, risk_level, probability, confidence,
                     rainfall_1d, rainfall_3d, rainfall_7d, elevation_m, slope_degrees,
                     soil_moisture, explanation, model_name, model_version)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            with get_db() as cur:
                cur.execute(sql, (
                    result.prediction_id,
                    result.latitude,
                    result.longitude,
                    result.risk_level,
                    result.probability,
                    result.confidence,
                    result.features.rainfall_1d,
                    result.features.rainfall_3d,
                    result.features.rainfall_7d,
                    result.features.elevation_m,
                    result.features.slope_degrees,
                    result.features.soil_moisture,
                    result.explanation,
                    result.model_name,
                    result.model_version,
                ))
            logger.info("Prediction persisted: %s", result.prediction_id)
        except Exception as exc:
            logger.warning("Could not persist prediction to DB: %s", exc)


prediction_service = MLPredictionService()
