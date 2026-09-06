from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List, Optional
from schemas.alert import AlertResponse
from services.alert_service import alert_service
from services.auth_service import require_roles

router = APIRouter()


@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(
    status: Optional[str] = Query(None, description="Filter by status: active, resolved, monitoring"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level: LOW, MEDIUM, HIGH, CRITICAL")
):
    """
    Get all landslide alerts calculated by the ML model.
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


@router.post("/alerts/sync")
async def sync_alerts_from_ml(
    user: dict = Depends(require_roles(["AUTHORITY", "ADMIN"]))
):
    """
    Trigger live ML evaluation across all monitored North East stations
    and synchronize risk statuses into the alerts database (Authority / Admin protected).
    """
    try:
        summary = await alert_service.sync_live_alerts_from_ml()
        return {
            "success": True,
            "message": "Live ML risk assessment completed across all NER stations.",
            "summary": summary,
            "triggered_by": user.get("full_name")
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to synchronize ML alerts: {str(e)}"
        )


@router.get("/dashboard/summary")
async def get_dashboard_summary():
    """
    Get real-time regional dashboard statistics, risk distribution,
    rainfall trend, and active alerts generated directly from ML predictions.
    """
    try:
        return await alert_service.get_regional_dashboard_summary()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate dashboard summary: {str(e)}"
        )


@router.get("/risk-zones")
async def get_risk_zones():
    """
    Get all monitored regional zones with their current ML-predicted risk levels
    and geographic coordinates for interactive map rendering.
    """
    try:
        return await alert_service.get_all_risk_zones()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch risk zones: {str(e)}"
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
