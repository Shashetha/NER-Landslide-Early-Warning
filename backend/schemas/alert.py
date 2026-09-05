from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class AlertBase(BaseModel):
    location: str
    latitude: float
    longitude: float
    risk_level: str
    probability: float
    affected_population: int
    description: str


class AlertResponse(AlertBase):
    id: int
    status: str
    created_at: str
    updated_at: str


class HazardReportRequest(BaseModel):
    location: str
    latitude: float
    longitude: float
    hazard_type: str
    severity: str
    description: str
    contact_info: Optional[str] = None


class HazardReportResponse(BaseModel):
    success: bool
    report_id: str
    message: str
    timestamp: str
