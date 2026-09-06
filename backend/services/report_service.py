import random
import string
import logging
from datetime import datetime
from typing import List

from database import get_db
from schemas.alert import HazardReportRequest, HazardReportResponse

logger = logging.getLogger(__name__)


def _generate_report_id() -> str:
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"report_{suffix}"


class ReportService:
    async def submit_report(self, report: HazardReportRequest) -> HazardReportResponse:
        report_id = _generate_report_id()
        sql = """
            INSERT INTO hazard_reports
                (id, location, latitude, longitude, hazard_type,
                 severity, description, contact_info, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending')
        """
        with get_db() as cur:
            cur.execute(sql, (
                report_id,
                report.location,
                report.latitude,
                report.longitude,
                report.hazard_type,
                report.severity,
                report.description,
                report.contact_info,
            ))

        logger.info("Hazard report saved: %s", report_id)

        return HazardReportResponse(
            success=True,
            report_id=report_id,
            message="Hazard report submitted successfully. Field team will investigate.",
            timestamp=datetime.utcnow().isoformat() + "Z",
        )

    async def get_all_reports(self) -> List[dict]:
        with get_db() as cur:
            cur.execute(
                "SELECT * FROM hazard_reports ORDER BY created_at DESC"
            )
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
                "contact_info": r["contact_info"],
                "status": r["status"],
                "created_at": r["created_at"].isoformat() + "Z",
            }
            for r in rows
        ]


report_service = ReportService()
