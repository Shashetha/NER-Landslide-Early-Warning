from fastapi import APIRouter, HTTPException
from schemas.prediction import LocationRequest, PredictionResponse
from services.prediction_service import prediction_service

router = APIRouter()


@router.post("/predictions", response_model=PredictionResponse)
async def predict_landslide_risk(location: LocationRequest):
    """
    Predict landslide risk for a given location using the trained Random Forest model.

    Required:
    - latitude, longitude

    Optional environmental inputs (estimated from distributions if not provided):
    - rainfall_1d  : 1-day cumulative rainfall (mm)
    - rainfall_3d  : 3-day cumulative rainfall (mm)
    - rainfall_7d  : 7-day cumulative rainfall (mm)
    - elevation_m  : elevation (meters)
    - slope_degrees: slope angle (degrees)
    - soil_moisture: volumetric soil moisture (%)

    Returns risk level (LOW / MEDIUM / HIGH / CRITICAL), probability, confidence,
    feature values, and a natural-language explanation.
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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/predictions/model-info")
async def get_model_info():
    """Get current ML model information and feature schema."""
    svc = prediction_service
    return {
        "model_name": svc.model_name,
        "model_version": svc.model_version,
        "status": "live" if svc._final_model is not None else "fallback",
        "description": (
            "Random Forest classifier trained on NER landslide events + background samples. "
            "Features: rainfall (1d/3d/7d), elevation, slope, soil moisture."
        ),
        "models_loaded": {
            "final_model": svc._final_model is not None,
            "rainfall_model": svc._rainfall_pkg is not None,
        },
        "required_inputs": {
            "latitude": "float (-90 to 90)",
            "longitude": "float (-180 to 180)",
        },
        "optional_inputs": {
            "rainfall_1d": "float — 1-day rainfall (mm)",
            "rainfall_3d": "float — 3-day rainfall (mm)",
            "rainfall_7d": "float — 7-day rainfall (mm)",
            "elevation_m": "float — elevation (m)",
            "slope_degrees": "float — slope angle (°)",
            "soil_moisture": "float — soil moisture (%)",
        },
        "output_format": {
            "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
            "probability": "float (0–1)",
            "confidence": "float (0–1)",
            "features": "EnvironmentalFeatures object",
            "explanation": "Natural-language risk explanation",
        },
    }
