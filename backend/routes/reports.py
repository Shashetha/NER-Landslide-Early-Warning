from fastapi import APIRouter, HTTPException
from typing import List
from schemas.alert import HazardReportRequest, HazardReportResponse
from services.report_service import report_service

router = APIRouter()


@router.post("/reports", response_model=HazardReportResponse)
async def submit_hazard_report(report: HazardReportRequest):
    """
    Submit a citizen/field officer hazard report.
    
    Report types:
    - landslide: Active landslide or mudflow
    - soil-erosion: Severe soil erosion
    - ground-cracks: Ground cracks or subsidence
    - rock-fall: Rock fall incidents
    
    Severity levels: low, medium, high
    """
    try:
        response = await report_service.submit_report(report)
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit report: {str(e)}"
        )


@router.get("/reports")
async def get_all_reports():
    """Get all submitted hazard reports"""
    try:
        reports = await report_service.get_all_reports()
        return {
            "total": len(reports),
            "reports": reports
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch reports: {str(e)}"
        )
