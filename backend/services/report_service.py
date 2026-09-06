"""
Field Report Service with Idempotent Offline Sync, Status Workflows, and Audit Logging.
"""

import random
import string
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import HTTPException

import database
from schemas.report import HazardReportCreate, HazardReportStatusUpdate, HazardReportResponse

logger = logging.getLogger(__name__)


def _generate_report_id() -> str:
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"rep_{suffix}"


class ReportService:
    async def submit_report(
        self,
        report: HazardReportCreate,
        user: Optional[dict] = None,
    ) -> Dict[str, Any]:
        """
        Submits field report with idempotency check to prevent duplicate syncs.
        Raises 503 if database pool is disconnected to prevent silent data loss.
        """
        if database._pool is None:
            raise HTTPException(
                status_code=503,
                detail="Database service unavailable. Report not saved on server."
            )

        report_id = _generate_report_id()

        with database.get_db() as cur:
            # 1. Check idempotency key for offline sync deduplication
            if report.idempotency_key:
                cur.execute("SELECT id, status, created_at FROM hazard_reports WHERE idempotency_key = %s LIMIT 1", (report.idempotency_key,))
                existing = cur.fetchone()
                if existing:
                    logger.info("Duplicate report submission prevented by idempotency key: %s", report.idempotency_key)
                    return {
                        "success": True,
                        "report_id": existing["id"],
                        "status": existing["status"],
                        "message": "Report already received and synchronized.",
                        "timestamp": existing["created_at"].isoformat() + "Z" if hasattr(existing["created_at"], "isoformat") else str(existing["created_at"]),
                    }

            # 2. Insert new report
            user_id = user["id"] if user else None
            reporter_name = report.reporter_name or (user["full_name"] if user else "Citizen")

            sql = """
                INSERT INTO hazard_reports
                    (id, user_id, reporter_name, contact_info, location, state, district,
                     latitude, longitude, hazard_type, severity, description,
                     visible_cracks, rockfall_observed, road_blocked, water_accumulation,
                     soil_movement, media_url, status, idempotency_key, sync_status, created_at)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s,
                     %s, %s, %s, %s,
                     %s, %s, 'NEW', %s, 'SYNCED', NOW())
            """
            cur.execute(sql, (
                report_id, user_id, reporter_name, report.contact_info, report.location, report.state, report.district,
                report.latitude, report.longitude, report.hazard_type, report.severity.lower(), report.description,
                bool(report.visible_cracks), bool(report.rockfall_observed), bool(report.road_blocked),
                bool(report.water_accumulation), bool(report.soil_movement), report.media_url,
                report.idempotency_key
            ))

            # 3. Create initial audit entry
            cur.execute(
                "INSERT INTO report_audit_logs (report_id, changed_by, old_status, new_status, notes, created_at) VALUES (%s, %s, %s, %s, %s, NOW())",
                (report_id, reporter_name, "NONE", "NEW", "Initial field report created")
            )

        return {
            "success": True,
            "report_id": report_id,
            "status": "NEW",
            "message": "Hazard report registered successfully with district emergency response team.",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    async def get_all_reports(
        self,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        state: Optional[str] = None,
    ) -> List[dict]:
        if database._pool is None:
            return []

        query = "SELECT * FROM hazard_reports WHERE 1=1"
        params = []
        if status:
            query += " AND status = %s"
            params.append(status.upper())
        if severity:
            query += " AND severity = %s"
            params.append(severity.lower())
        if state:
            query += " AND state = %s"
            params.append(state)

        query += " ORDER BY created_at DESC"

        with database.get_db() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

        return [
            {
                "id": r["id"],
                "location": r["location"],
                "latitude": float(r["latitude"]),
                "longitude": float(r["longitude"]),
                "hazard_type": r["hazard_type"],
                "severity": r["severity"],
                "description": r["description"],
                "status": r["status"],
                "visible_cracks": bool(r.get("visible_cracks")),
                "rockfall_observed": bool(r.get("rockfall_observed")),
                "road_blocked": bool(r.get("road_blocked")),
                "water_accumulation": bool(r.get("water_accumulation")),
                "soil_movement": bool(r.get("soil_movement")),
                "media_url": r.get("media_url"),
                "admin_notes": r.get("admin_notes"),
                "reporter_name": r.get("reporter_name"),
                "contact_info": r.get("contact_info"),
                "state": r.get("state"),
                "district": r.get("district"),
                "created_at": r["created_at"].isoformat() + "Z",
                "updated_at": r["updated_at"].isoformat() + "Z" if r.get("updated_at") else None,
            }
            for r in rows
        ]

    async def update_report_status(
        self,
        report_id: str,
        update: HazardReportStatusUpdate,
        user: dict,
    ) -> Dict[str, Any]:
        """
        Disaster governance workflow: update status with mandatory audit log.
        """
        if database._pool is None:
            raise HTTPException(status_code=503, detail="Database service unavailable")

        with database.get_db() as cur:
            cur.execute("SELECT status FROM hazard_reports WHERE id = %s", (report_id,))
            row = cur.fetchone()
            if not row:
                return {"success": False, "message": "Report not found"}

            old_status = row["status"]
            new_status = update.status.upper()

            cur.execute(
                """
                UPDATE hazard_reports
                SET status = %s, admin_notes = %s, updated_at = NOW()
                WHERE id = %s
                """,
                (new_status, update.admin_notes, report_id)
            )

            # Insert audit trail
            cur.execute(
                """
                INSERT INTO report_audit_logs (report_id, changed_by, old_status, new_status, notes, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
                """,
                (report_id, user.get("full_name", "Authority"), old_status, new_status, update.admin_notes)
            )

        return {
            "success": True,
            "report_id": report_id,
            "old_status": old_status,
            "new_status": new_status,
            "updated_by": user.get("full_name"),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }


report_service = ReportService()
