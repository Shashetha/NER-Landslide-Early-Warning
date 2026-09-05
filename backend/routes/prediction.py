from fastapi import APIRouter, HTTPException
from schemas.prediction import LocationRequest, PredictionResponse
from services.prediction_service import prediction_service

router = APIRouter()


@router.post("/predictions", response_model=PredictionResponse)
async def predict_landslide_risk(location: LocationRequest):
    """
    Predict landslide risk for a given location.
    
    This endpoint analyzes environmental factors and returns:
    - Risk level (LOW, MEDIUM, HIGH, CRITICAL)
    - Probability score (0-1)
    - Environmental features (rainfall, slope, elevation, soil moisture, temperature)
    - Explanation of risk factors
    
    TODO: When ML model is ready from Team A+B:
    1. Replace MockPredictionService with real ML model
    2. Integrate actual environmental data APIs
    3. Add database logging for predictions
    """
    try:
        prediction = await prediction_service.predict_landslide_risk(
            latitude=location.latitude,
            longitude=location.longitude
        )
        return prediction
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/predictions/model-info")
async def get_model_info():
    """Get current ML model information"""
    return {
        "model_name": prediction_service.model_name,
        "model_version": prediction_service.model_version,
        "status": "mock",
        "description": "Mock prediction service. Replace with real ML model.",
        "required_inputs": {
            "latitude": "float (-90 to 90)",
            "longitude": "float (-180 to 180)"
        },
        "output_format": {
            "risk_level": "string (LOW, MEDIUM, HIGH, CRITICAL)",
            "probability": "float (0-1)",
            "confidence": "float (0-1)",
            "features": {
                "rainfall": "float (mm)",
                "slope": "float (degrees)",
                "elevation": "float (meters)",
                "soil_moisture": "float (%)",
                "temperature": "float (°C)"
            }
        }
    }
