from typing import Optional, List
from pydantic import BaseModel, Field


class LocationRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    rainfall_1d: Optional[float] = Field(None, description="1-day rainfall (mm)")
    rainfall_3d: Optional[float] = Field(None, description="3-day rainfall (mm)")
    rainfall_7d: Optional[float] = Field(None, description="7-day rainfall (mm)")
    elevation_m: Optional[float] = Field(None, description="Elevation (m)")
    slope_degrees: Optional[float] = Field(None, description="Slope angle (degrees)")
    soil_moisture: Optional[float] = Field(
        None,
        description="Soil moisture — volumetric FRACTION 0–1 (e.g. 0.35, NOT 35)"
    )


class EnvironmentalFeatures(BaseModel):
    rainfall_1d: Optional[float] = Field(None, description="mm")
    rainfall_3d: Optional[float] = Field(None, description="mm")
    rainfall_7d: Optional[float] = Field(None, description="mm")
    elevation_m: Optional[float] = Field(None, description="m")
    slope_degrees: Optional[float] = Field(None, description="degrees")
    soil_moisture: Optional[float] = Field(None, description="fraction 0–1")


class PredictionResponse(BaseModel):
    prediction_id: str
    latitude: float
    longitude: float
    risk_level: str
    probability: float
    confidence: float = Field(
        description="Statistical prediction confidence based on ensemble tree agreement (0.5 to 1.0)"
    )
    features: EnvironmentalFeatures
    features_imputed: bool = Field(
        description="True if any feature was filled by the model imputer (data unavailable)"
    )
    is_mock: bool = Field(
        description="True if providers returned no data and imputer medians were used for ALL features"
    )
    explanation: str
    model_name: str = "landslide-rf-final"
    model_version: str = "1.0.0"
    timestamp: str


# -------------------------------------------------------------
# FUTURE MULTI-HAZARD FORECAST SCHEMAS (24h, 48h, 72h, 7-Day)
# -------------------------------------------------------------
class ForecastWindow(BaseModel):
    horizon: str  # "Current", "+24h", "+48h", "+72h", "+7d"
    date_label: str
    landslide_probability: float
    landslide_risk_level: str
    rainfall_surge_mm: float
    cumulative_3d_rain_mm: float
    soil_moisture_pct: float
    flash_flood_risk: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    flood_susceptibility_score: float
    river_discharge_m3s: Optional[float] = None
    advisory: str


class MultiHazardForecastResponse(BaseModel):
    latitude: float
    longitude: float
    elevation_m: float
    slope_degrees: float
    current_assessment: PredictionResponse
    forecast_24h: ForecastWindow
    forecast_48h: ForecastWindow
    forecast_72h: ForecastWindow
    timeline_7d: List[ForecastWindow]
    peak_hazard_day: str
    peak_hazard_type: str
    summary_advisory: str
    model_name: str = "landslide-rf-final"
    generated_at: str
