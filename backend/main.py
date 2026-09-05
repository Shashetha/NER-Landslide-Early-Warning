from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import random
import string
from datetime import datetime, timedelta

app = FastAPI(
    title="Landslide Risk Monitoring API",
    description="AI-powered landslide risk prediction and early warning system for North East India",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schemas
class LocationRequest(BaseModel):
    latitude: float
    longitude: float

class HazardReportRequest(BaseModel):
    location: str
    latitude: float
    longitude: float
    hazard_type: str
    severity: str
    description: str
    contact_info: Optional[str] = None

# Mock DB
MOCK_ALERTS = [
    {
        "id": 1,
        "location": "Gangtok, Sikkim",
        "latitude": 27.3389,
        "longitude": 88.6065,
        "risk_level": "HIGH",
        "probability": 0.87,
        "status": "active",
        "affected_population": 2500,
        "description": "Heavy rainfall detected in the area with steep slope conditions.",
        "created_at": (datetime.utcnow() - timedelta(hours=2)).isoformat() + "Z",
        "updated_at": (datetime.utcnow() - timedelta(minutes=12)).isoformat() + "Z"
    },
    {
        "id": 2,
        "location": "Cherrapunji, Meghalaya",
        "latitude": 25.2630,
        "longitude": 91.7324,
        "risk_level": "CRITICAL",
        "probability": 0.94,
        "status": "active",
        "affected_population": 5200,
        "description": "Critical conditions detected. Multiple risk factors present in wettest place on Earth.",
        "created_at": (datetime.utcnow() - timedelta(hours=4)).isoformat() + "Z",
        "updated_at": (datetime.utcnow() - timedelta(minutes=30)).isoformat() + "Z"
    },
    {
        "id": 3,
        "location": "Itanagar, Arunachal Pradesh",
        "latitude": 27.0844,
        "longitude": 93.6053,
        "risk_level": "HIGH",
        "probability": 0.79,
        "status": "active",
        "affected_population": 1800,
        "description": "Elevated soil moisture levels detected in hilly terrain.",
        "created_at": (datetime.utcnow() - timedelta(hours=6)).isoformat() + "Z",
        "updated_at": (datetime.utcnow() - timedelta(minutes=45)).isoformat() + "Z"
    },
    {
        "id": 4,
        "location": "Shillong, Meghalaya",
        "latitude": 25.5788,
        "longitude": 91.8933,
        "risk_level": "MEDIUM",
        "probability": 0.62,
        "status": "resolved",
        "affected_population": 3100,
        "description": "Risk levels have decreased. Situation stabilized.",
        "created_at": (datetime.utcnow() - timedelta(hours=48)).isoformat() + "Z",
        "updated_at": (datetime.utcnow() - timedelta(hours=12)).isoformat() + "Z"
    }
]

MOCK_REPORTS = []

# Routes
@app.get("/")
def root():
    return {
        "message": "Landslide Risk Monitoring API is running",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/api/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# Predictions API
@app.post("/api/v1/predictions")
def predict_landslide_risk(location: LocationRequest):
    rainfall = round(random.uniform(50, 250), 2)
    slope = round(random.uniform(10, 50), 2)
    elevation = round(random.uniform(500, 2500), 2)
    soil_moisture = round(random.uniform(30, 80), 2)
    temperature = round(random.uniform(10, 25), 2)

    base_probability = random.uniform(0.3, 0.95)
    if rainfall > 150 and slope > 30:
        base_probability = min(base_probability + 0.15, 0.99)
    if soil_moisture > 70:
        base_probability = min(base_probability + 0.10, 0.99)

    probability = round(base_probability, 2)
    confidence = round(random.uniform(0.80, 0.95), 2)

    if probability >= 0.85:
        risk_level = "CRITICAL"
    elif probability >= 0.7:
        risk_level = "HIGH"
    elif probability >= 0.5:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    explanations = {
        "LOW": "Current environmental conditions indicate stable terrain with minimal landslide risk.",
        "MEDIUM": f"Moderate risk detected. Rainfall of {rainfall}mm with {slope}° slope requires close monitoring.",
        "HIGH": f"High rainfall ({rainfall}mm) combined with steep terrain ({slope}°) is increasing landslide probability.",
        "CRITICAL": f"CRITICAL RISK. Heavy rainfall ({rainfall}mm), steep slope ({slope}°), and saturated soil ({soil_moisture}%)."
    }

    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

    return {
        "prediction_id": f"pred_{random_str}",
        "latitude": location.latitude,
        "longitude": location.longitude,
        "risk_level": risk_level,
        "probability": probability,
        "confidence": confidence,
        "features": {
            "rainfall": rainfall,
            "slope": slope,
            "elevation": elevation,
            "soil_moisture": soil_moisture,
            "temperature": temperature
        },
        "explanation": explanations.get(risk_level, "Risk assessment completed."),
        "model_name": "landslide-model-mock",
        "model_version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/api/v1/alerts")
def get_alerts(status: Optional[str] = None, risk_level: Optional[str] = None):
    alerts = MOCK_ALERTS.copy()
    if status:
        alerts = [a for a in alerts if a["status"] == status]
    if risk_level:
        alerts = [a for a in alerts if a["risk_level"] == risk_level]
    return alerts

@app.post("/api/v1/reports")
def submit_report(report: HazardReportRequest):
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    report_id = f"report_{random_str}"
    
    report_data = {
        "id": report_id,
        "location": report.location,
        "latitude": report.latitude,
        "longitude": report.longitude,
        "hazard_type": report.hazard_type,
        "severity": report.severity,
        "description": report.description,
        "contact_info": report.contact_info,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    MOCK_REPORTS.append(report_data)
    
    return {
        "success": True,
        "report_id": report_id,
        "message": "Hazard report submitted successfully. Field team will investigate.",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/api/v1/reports")
def get_reports():
    return {
        "total": len(MOCK_REPORTS),
        "reports": MOCK_REPORTS
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
