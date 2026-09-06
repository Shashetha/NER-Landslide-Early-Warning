from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from services.proximity_alert_service import proximity_alert_service
from services.notification_service import notification_service
from services.auth_service import require_roles
from providers.notifications import sms_provider, email_provider
from data.ner_locations import NER_MONITORED_LOCATIONS

router = APIRouter()


class TargetedDispatchModalRequest(BaseModel):
    state: str = Field(..., description="Target NER State (e.g. Sikkim, Meghalaya, etc.)")
    area: str = Field(..., description="Target Location / Area Name")
    risk_level: str = Field("CRITICAL", description="LOW, MEDIUM, HIGH, CRITICAL")
    probability: float = Field(0.95, ge=0.0, le=1.0)
    custom_message: Optional[str] = None
    radius_km: Optional[float] = 50.0


@router.get("/notifications/targeted-stations")
async def get_targeted_stations_by_state(state: Optional[str] = None):
    if state and state.strip() and state != "All States":
        stations = [s for s in NER_MONITORED_LOCATIONS if s["state"].lower() == state.lower()]
    else:
        stations = NER_MONITORED_LOCATIONS

    return {
        "total": len(stations),
        "stations": [
            {
                "id": s["id"],
                "name": s["name"],
                "state": s["state"],
                "latitude": s["latitude"],
                "longitude": s["longitude"],
                "elevation_m": s.get("elevation_m"),
                "slope_degrees": s.get("slope_degrees"),
            }
            for s in stations
        ]
    }


@router.post("/notifications/targeted-dispatch")
async def authority_targeted_emergency_dispatch(
    req: TargetedDispatchModalRequest,
    user: dict = Depends(require_roles(["AUTHORITY", "ADMIN"]))
):
    """
    AUTHORITY EMERGENCY FEATURE:
    Dispatches early warning SMS strictly to UNIQUE registered recipients in the selected area.
    Filters out any duplicate phone numbers automatically.
    """
    import database

    if database._pool is None:
        raise HTTPException(status_code=503, detail="Database service unavailable")

    target_recipients = []
    with database.get_db() as cur:
        cur.execute(
            """
            SELECT id, full_name, phone_number, email, role, state, district 
            FROM users 
            WHERE is_active = TRUE 
              AND (LOWER(state) = LOWER(%s) OR role IN ('ADMIN', 'AUTHORITY'))
            ORDER BY id ASC
            """,
            (req.state,)
        )
        raw_recipients = cur.fetchall()
        
        seen_numbers = set()
        for r in raw_recipients:
            num = r.get("phone_number")
            if num and num not in seen_numbers:
                seen_numbers.add(num)
                target_recipients.append(r)

    if not target_recipients:
        raise HTTPException(
            status_code=404,
            detail=f"No active registered citizens or field responders found for state: {req.state}."
        )

    prob_pct = int(req.probability * 100)
    location_label = f"{req.area}, {req.state}"
    
    default_msg = (
        f"GOVT DISASTER ALERT: [{req.risk_level.upper()} RISK ({prob_pct}%)] "
        f"Imminent landslide hazard detected at {location_label}. "
        f"Evacuate steep slope cuts. Follow local SDMA/NDMA advisories."
    )
    final_sms_text = req.custom_message.strip() if req.custom_message and req.custom_message.strip() else default_msg

    sent_count = 0
    dispatched_list = []

    for r in target_recipients:
        phone = r.get("phone_number")
        if not phone:
            continue

        sms_res = await sms_provider.send_sms(phone, final_sms_text)
        if sms_res.get("success"):
            sent_count += 1
            dispatched_list.append(phone)

        with database.get_db() as cur:
            cur.execute(
                """
                INSERT INTO notification_logs (alert_id, channel, recipient, recipient_role, message, status, created_at)
                VALUES (NULL, 'SMS', %s, %s, %s, %s, NOW())
                """,
                (phone, r.get("role", "CITIZEN"), final_sms_text[:500], "SENT" if sms_res.get("success") else "FAILED")
            )

    return {
        "success": True,
        "state": req.state,
        "area": req.area,
        "risk_level": req.risk_level,
        "probability": req.probability,
        "recipients_targeted": len(target_recipients),
        "sms_delivered": sent_count,
        "dispatched_numbers": list(set(dispatched_list)),
        "message": final_sms_text,
        "dispatched_by": user.get("full_name")
    }


@router.get("/notifications/logs")
async def get_notification_logs(
    limit: int = 50,
    user: dict = Depends(require_roles(["AUTHORITY", "ADMIN"]))
):
    return await notification_service.get_notification_logs(limit=limit)
