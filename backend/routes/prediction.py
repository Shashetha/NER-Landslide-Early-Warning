import logging
import os
from fastapi import APIRouter, HTTPException, Query
from schemas.prediction import LocationRequest, PredictionResponse, MultiHazardForecastResponse
from services.prediction_service import prediction_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/predictions", response_model=PredictionResponse)
async def predict_landslide_risk(location: LocationRequest):
    """
    Predict landslide risk for a given location using the trained Random Forest model.
    """
    try:
        prediction = await prediction_service.predict_landslide_risk(
            latitude=location.latitude,
            longitude=location.longitude,
            rainfall_1d=location.rainfall_1d,
            rainfall_3d=location.rainfall_3d,
            rainfall_7d=location.rainfall_7d,
            elevation_m=location.elevation_m,
            slope_degrees=location.slope_degrees,
            soil_moisture=location.soil_moisture,
        )
        return prediction
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error("Prediction failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/predictions/multi-hazard-forecast", response_model=MultiHazardForecastResponse)
async def predict_multi_hazard_forecast(location: LocationRequest):
    """
    FUTURE RISK PREDICTION ENGINE:
    Evaluates rolling multi-day ML model inference for:
    - 24-hour Landslide Risk Forecast
    - 48-hour Landslide Risk Forecast
    - 72-hour Landslide Risk Forecast
    - 7-Day Rainfall Surge (mm) & Soil Saturation
    - 7-Day Flash Flood Susceptibility Score & Risk Level
    """
    try:
        return await prediction_service.predict_multi_hazard_forecast(
            latitude=location.latitude,
            longitude=location.longitude
        )
    except Exception as e:
        logger.error("Multi-hazard forecast failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Multi-hazard forecast failed: {str(e)}")


@router.get("/predictions/model-info")
async def get_model_info():
    """Get current ML model metadata and feature specification."""
    from ml.FEATURES import (
        FEATURE_NAMES, FEATURE_UNITS, FEATURE_TRAINING_RANGES,
        IMPUTER_MEDIANS, RISK_THRESHOLDS
    )
    svc = prediction_service
    return {
        "model_name": svc.model_name,
        "model_version": svc.model_version,
        "status": "live" if svc._model is not None else "unavailable",
        "features": {
            name: {
                "unit": FEATURE_UNITS[name],
                "training_range": list(FEATURE_TRAINING_RANGES[name]),
                "imputer_median": IMPUTER_MEDIANS[name],
            }
            for name in FEATURE_NAMES
        },
        "feature_order": FEATURE_NAMES,
        "risk_thresholds": RISK_THRESHOLDS,
        "soil_moisture_scale": "fraction (0.0 - 1.0, volumetric m3/m3)",
    }
