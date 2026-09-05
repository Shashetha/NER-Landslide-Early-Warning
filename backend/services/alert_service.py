from datetime import datetime, timedelta
from typing import List
from schemas.alert import AlertResponse

MOCK_ALERTS_DB = [
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


class AlertService:
    async def get_all_alerts(self, status: str = None, risk_level: str = None) -> List[AlertResponse]:
        alerts = MOCK_ALERTS_DB.copy()
        if status:
            alerts = [a for a in alerts if a["status"] == status]
        if risk_level:
            alerts = [a for a in alerts if a["risk_level"] == risk_level]
        return [AlertResponse(**alert) for alert in alerts]
    
    async def get_alert_by_id(self, alert_id: int) -> AlertResponse:
        alert = next((a for a in MOCK_ALERTS_DB if a["id"] == alert_id), None)
        if alert:
            return AlertResponse(**alert)
        return None


alert_service = AlertService()
