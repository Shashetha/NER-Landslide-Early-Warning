"""
Automated Multi-Channel Emergency Dispatch (SMS via TextBee & Email).
Targeting local residents and disaster officers in affected NER states/districts.
"""

import hashlib
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

import database
from providers.notifications import sms_provider, email_provider

logger = logging.getLogger(__name__)

ALERT_COOLDOWN_MINUTES = 60  # Prevent spamming the same location within 1 hour


class NotificationService:
    @staticmethod
    def generate_dedup_hash(location: str, risk_level: str) -> str:
        date_str = datetime.utcnow().strftime("%Y-%m-%d-%H")
        raw = f"{location.strip().lower()}:{risk_level.upper()}:{date_str}"
        return hashlib.sha256(raw.encode()).hexdigest()

    async def broadcast_landslide_warning(
        self,
        alert_id: Optional[int],
        location: str,
        risk_level: str,
        probability: float,
        description: str,
        state: Optional[str] = None,
        district: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Broadcasts early warning across TextBee SMS and Email to all users registered in the affected state/district.
        """
        if risk_level.upper() not in ("HIGH", "CRITICAL"):
            logger.info("Risk level %s is below broadcast threshold (HIGH/CRITICAL) for %s", risk_level, location)
            return {"success": True, "status": "SKIPPED_LOW_RISK"}

        dedup_hash = self.generate_dedup_hash(location, risk_level)

        # 1. Deduplication Cooldown Check
        if database._pool is not None:
            with database.get_db() as cur:
                cur.execute(
                    """
                    SELECT id FROM notification_logs
                    WHERE dedup_hash = %s AND created_at > DATE_SUB(NOW(), INTERVAL %s MINUTE)
                    LIMIT 1
                    """,
                    (dedup_hash, ALERT_COOLDOWN_MINUTES)
                )
                if cur.fetchone():
                    logger.info("Emergency broadcast suppressed by cooldown for %s (%s)", location, risk_level)
                    return {"success": True, "status": "DEDUPLICATED"}

        prob_pct = int(probability * 100)

        # 2. Dynamic multi-channel message derived from live prediction explanation
        sms_msg = (
            f"GOVT DISASTER ALERT: [{risk_level.upper()} RISK ({prob_pct}%)] Landslide threat at {location}. "
            f"Evacuate steep slope cuts. Follow local SDMA/NDMA advisories."
        )

        email_subject = f"EMERGENCY ALERT: {risk_level.upper()} Landslide Risk Detected at {location}"
        email_html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 2px solid #dc2626; border-radius: 8px; overflow: hidden;">
            <div style="background: #dc2626; color: #ffffff; padding: 20px; text-align: center;">
                <h1 style="margin: 0; font-size: 24px;">🚨 LANDSLIDE EARLY WARNING</h1>
                <p style="margin: 5px 0 0; font-size: 14px; text-transform: uppercase;">North Eastern Region Disaster Management</p>
            </div>
            <div style="padding: 24px; background: #ffffff;">
                <h2 style="color: #0f172a; margin-top: 0;">Location: {location}</h2>
                <div style="background: #fee2e2; border-left: 4px solid #dc2626; padding: 12px; margin-bottom: 20px;">
                    <strong style="color: #991b1b; font-size: 18px;">Threat Level: {risk_level.upper()} ({prob_pct}%)</strong>
                </div>
                <p style="font-size: 15px; color: #334155; line-height: 1.6;"><strong>Observation:</strong> {description}</p>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 16px; margin-top: 20px;">
                    <h3 style="margin-top: 0; color: #0f172a;">Recommended Public Action:</h3>
                    <ul style="color: #475569; font-size: 14px; line-height: 1.6;">
                        <li>Avoid travel across vulnerable hill highway corridors.</li>
                        <li>Report visible ground fissures or boulder movements immediately.</li>
                        <li>Keep emergency grab-bags and communications ready.</li>
                    </ul>
                </div>
            </div>
            <div style="background: #0f172a; color: #94a3b8; padding: 12px; text-align: center; font-size: 12px;">
                Automated AI Landslide Monitoring Platform - Government of India
            </div>
        </div>
        """

        # 3. Query target recipients from real MySQL database
        recipients = []
        if database._pool is not None:
            with database.get_db() as cur:
                query = "SELECT id, full_name, email, phone_number, role, state, district FROM users WHERE is_active = TRUE"
                params = []
                if state:
                    query += " AND (state = %s OR state IS NULL OR role IN ('ADMIN', 'AUTHORITY'))"
                    params.append(state)
                cur.execute(query, params)
                recipients = cur.fetchall()

        if not recipients:
            logger.warning("No registered recipients in database for state %s. Dispatch skipped.", state)
            return {"success": False, "status": "NO_RECIPIENTS"}

        sms_count = 0
        email_count = 0

        # 4. Dispatch TextBee SMS & Email
        for r in recipients:
            phone = r.get("phone_number")
            email = r.get("email")

            if phone:
                sms_res = await sms_provider.send_sms(phone, sms_msg)
                if sms_res.get("success"):
                    sms_count += 1
                self._log_notification(alert_id, "SMS", phone, r.get("role"), sms_msg, "SENT" if sms_res.get("success") else "FAILED", dedup_hash)

            if email:
                email_res = await email_provider.send_email(email, email_subject, email_html)
                if email_res.get("success"):
                    email_count += 1
                self._log_notification(alert_id, "EMAIL", email, r.get("role"), email_subject, "SENT" if email_res.get("success") else "FAILED", dedup_hash)

        logger.info(
            "Emergency dispatch completed for %s: %d SMS, %d Emails sent to %d regional residents",
            location, sms_count, email_count, len(recipients)
        )

        return {
            "success": True,
            "status": "DISPATCHED",
            "recipients_targeted": len(recipients),
            "sms_sent": sms_count,
            "emails_sent": email_count,
            "dedup_hash": dedup_hash,
        }

    def _log_notification(self, alert_id, channel, recipient, role, message, status, dedup_hash):
        if database._pool is not None:
            try:
                with database.get_db() as cur:
                    cur.execute(
                        """
                        INSERT INTO notification_logs
                            (alert_id, channel, recipient, recipient_role, message, status, dedup_hash, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                        """,
                        (alert_id, channel, recipient, role or "CITIZEN", message[:500], status, dedup_hash)
                    )
            except Exception as e:
                logger.warning("Could not log notification: %s", e)

    async def get_notification_logs(self, limit: int = 50) -> List[dict]:
        if database._pool is None:
            return []
        with database.get_db() as cur:
            cur.execute("SELECT * FROM notification_logs ORDER BY created_at DESC LIMIT %s", (limit,))
            rows = cur.fetchall()
            return [
                {
                    "id": r["id"],
                    "alert_id": r["alert_id"],
                    "channel": r["channel"],
                    "recipient": r["recipient"],
                    "recipient_role": r["recipient_role"],
                    "message": r["message"],
                    "status": r["status"],
                    "created_at": r["created_at"].isoformat() + "Z" if hasattr(r["created_at"], "isoformat") else str(r["created_at"]),
                }
                for r in rows
            ]


notification_service = NotificationService()
