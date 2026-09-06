from typing import Optional
from pydantic import BaseModel, Field


class LocationRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    rainfall_1d: Optional[float] = Field(None, description="Rainfall in last 1 day (mm)")
    rainfall_3d: Optional[float] = Field(None, description="Rainfall in last 3 days (mm)")
    rainfall_7d: Optional[float] = Field(None, description="Rainfall in last 7 days (mm)")
    elevation_m: Optional[float] = Field(None, description="Elevation in meters")
    slope_degrees: Optional[float] = Field(None, description="Slope angle in degrees")
    soil_moisture: Optional[float] = Field(None, description="Soil moisture (%)")


class EnvironmentalFeatures(BaseModel):
    rainfall_1d: float
    rainfall_3d: float
    rainfall_7d: float
    elevation_m: float
    slope_degrees: float
    soil_moisture: float


class PredictionResponse(BaseModel):
    prediction_id: str
    latitude: float
    longitude: float
    risk_level: str
    probability: float
    confidence: float
    features: EnvironmentalFeatures
    explanation: str
    model_name: str = "landslide-rf-final"
    model_version: str = "1.0.0"
    timestamp: str
