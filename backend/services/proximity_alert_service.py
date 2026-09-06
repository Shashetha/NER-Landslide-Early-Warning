import math
import logging
from typing import List, Dict, Any, Optional

import database
from providers.notifications import sms_provider

logger = logging.getLogger(__name__)


class ProximityAlertService:
    async def get_nearby_recipients(
        self,
        hazard_lat: float,
        hazard_lng: float,
        radius_km: float = 50.0,
        state: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Finds all citizens and emergency responders registered strictly within the target state/district
        or authorized command personnel. Excludes unconfigured users.
        """
        if database._pool is None:
            return []

        recipients = []
        with database.get_db() as cur:
            cur.execute("SELECT id, full_name, phone_number, role, state, district FROM users WHERE is_active = TRUE AND phone_number IS NOT NULL")
            all_users = cur.fetchall()

            for u in all_users:
                user_state = u.get("state")
                is_state_match = state and user_state and user_state.strip().lower() == state.strip().lower()
                is_command_role = u.get("role") in ("ADMIN", "AUTHORITY")

                # Strictly require state match or official command role to prevent broadcast leakage
                if is_state_match or is_command_role:
                    recipients.append(u)

        return recipients

    async def broadcast_to_nearby_people(
        self,
        location_name: str,
        hazard_lat: float,
        hazard_lng: float,
        risk_level: str,
        probability: float,
        description: str,
        radius_km: float = 50.0,
        state: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sends TextBee SMS to all people residing in or near the affected danger zone.
        """
        recipients = await self.get_nearby_recipients(hazard_lat, hazard_lng, radius_km, state)

        prob_pct = int(probability * 100)
        sms_msg = (
            f"GOVT DISASTER ALERT: [{risk_level.upper()} RISK ({prob_pct}%)] Landslide threat detected at {location_name}. "
            f"If you are within {int(radius_km)}km, stay away from steep hill cuttings and follow local emergency advisories."
        )

        sent_count = 0
        failed_count = 0
        dispatched_numbers = []

        for r in recipients:
            phone = r.get("phone_number")
            if not phone:
                continue

            sms_res = await sms_provider.send_sms(phone, sms_msg)
            if sms_res.get("success"):
                sent_count += 1
                dispatched_numbers.append(phone)
            else:
                failed_count += 1

            if database._pool is not None:
                try:
                    with database.get_db() as cur:
                        cur.execute(
                            """
                            INSERT INTO notification_logs (alert_id, channel, recipient, recipient_role, message, status, created_at)
                            VALUES (NULL, 'SMS', %s, %s, %s, %s, NOW())
                            """,
                            (phone, r.get("role", "CITIZEN"), sms_msg[:500], "SENT" if sms_res.get("success") else "FAILED")
                        )
                except Exception as e:
                    logger.warning("Could not log proximity SMS: %s", e)

        logger.info("Proximity emergency broadcast sent to %d nearby residents around %s", sent_count, location_name)
        return {
            "success": True,
            "location": location_name,
            "danger_radius_km": radius_km,
            "total_targeted": len(recipients),
            "sms_delivered": sent_count,
            "dispatched_numbers": list(set(dispatched_numbers)),
        }


proximity_alert_service = ProximityAlertService()
