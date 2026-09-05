from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class LocationRequest(BaseModel):
    latitude: float
    longitude: float


class EnvironmentalFeatures(BaseModel):
    rainfall: float
    slope: float
    elevation: float
    soil_moisture: float
    temperature: float


class PredictionResponse(BaseModel):
    prediction_id: str
    latitude: float
    longitude: float
    risk_level: str
    probability: float
    confidence: float
    features: EnvironmentalFeatures
    explanation: str
    model_name: str = "landslide-model-mock"
    model_version: str = "1.0.0"
    timestamp: str
