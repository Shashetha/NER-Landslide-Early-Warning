from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from schemas.alert import AlertResponse
from services.alert_service import alert_service

router = APIRouter()


@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(
    status: Optional[str] = Query(None, description="Filter by status: active, resolved"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level: LOW, MEDIUM, HIGH, CRITICAL")
):
    """
    Get all landslide alerts.
    
    Supports filtering by:
    - status (active, resolved)
    - risk_level (LOW, MEDIUM, HIGH, CRITICAL)
    """
    try:
        alerts = await alert_service.get_all_alerts(
            status=status,
            risk_level=risk_level
        )
        return alerts
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch alerts: {str(e)}"
        )


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
async def get_alert_by_id(alert_id: int):
    """Get specific alert details by ID"""
    alert = await alert_service.get_alert_by_id(alert_id)
    if not alert:
        raise HTTPException(
            status_code=404,
            detail=f"Alert with ID {alert_id} not found"
        )
    return alert
