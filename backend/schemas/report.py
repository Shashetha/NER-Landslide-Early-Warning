from typing import Optional, List
from pydantic import BaseModel, Field


class HazardReportCreate(BaseModel):
    location: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    hazard_type: str = "landslide"
    severity: str = "medium"
    description: str
    reporter_name: Optional[str] = None
    contact_info: Optional[str] = None
    visible_cracks: Optional[bool] = False
    rockfall_observed: Optional[bool] = False
    road_blocked: Optional[bool] = False
    water_accumulation: Optional[bool] = False
    soil_movement: Optional[bool] = False
    media_url: Optional[str] = None
    idempotency_key: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None


class HazardReportStatusUpdate(BaseModel):
    status: str = Field(..., description="NEW, UNDER_REVIEW, VERIFIED, ACTION_REQUIRED, RESOLVED, REJECTED")
    admin_notes: Optional[str] = None


class HazardReportResponse(BaseModel):
    id: str
    location: str
    latitude: float
    longitude: float
    hazard_type: str
    severity: str
    description: str
    status: str
    visible_cracks: bool = False
    rockfall_observed: bool = False
    road_blocked: bool = False
    water_accumulation: bool = False
    soil_movement: bool = False
    media_url: Optional[str] = None
    admin_notes: Optional[str] = None
    reporter_name: Optional[str] = None
    contact_info: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None
