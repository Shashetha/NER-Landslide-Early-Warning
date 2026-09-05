import random
import string
from datetime import datetime
from typing import List
from schemas.alert import HazardReportRequest, HazardReportResponse

MOCK_REPORTS_DB = []


class ReportService:
    def generate_report_id(self) -> str:
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"report_{random_str}"
    
    async def submit_report(self, report: HazardReportRequest) -> HazardReportResponse:
        report_id = self.generate_report_id()
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
        MOCK_REPORTS_DB.append(report_data)
        
        return HazardReportResponse(
            success=True,
            report_id=report_id,
            message="Hazard report submitted successfully. Field team will investigate.",
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    
    async def get_all_reports(self) -> List[dict]:
        return MOCK_REPORTS_DB


report_service = ReportService()
