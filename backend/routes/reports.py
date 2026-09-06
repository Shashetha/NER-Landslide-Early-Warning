import os
import uuid
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File

from schemas.report import HazardReportCreate, HazardReportStatusUpdate, HazardReportResponse
from services.report_service import report_service
from services.auth_service import get_current_user, require_roles

router = APIRouter()

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/reports")
async def submit_hazard_report(
    report: HazardReportCreate,
    user: Optional[dict] = Depends(get_current_user)
):
    """
    Submit a citizen or field officer hazard report with offline sync idempotency.
    """
    return await report_service.submit_report(report=report, user=user)


@router.post("/reports/upload-media")
async def upload_report_media(file: UploadFile = File(...)):
    """
    Secure file upload: Validates extensions, enforces size limit, and sanitizes filenames.
    """
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    unique_filename = f"{uuid.uuid4().hex}{ext}"
    filepath = UPLOAD_DIR / unique_filename

    bytes_written = 0
    with open(filepath, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            bytes_written += len(chunk)
            if bytes_written > MAX_FILE_SIZE:
                buffer.close()
                filepath.unlink(missing_ok=True)
                raise HTTPException(status_code=400, detail="File exceeds maximum allowed size limit of 10MB")
            buffer.write(chunk)

    return {"media_url": f"/uploads/{unique_filename}", "filename": unique_filename}


@router.get("/reports")
async def get_all_reports(
    status: Optional[str] = Query(None, description="NEW, UNDER_REVIEW, VERIFIED, ACTION_REQUIRED, RESOLVED, REJECTED"),
    severity: Optional[str] = Query(None, description="low, medium, high, critical"),
    state: Optional[str] = Query(None, description="Filter by NER State"),
):
    """
    Get all submitted field and citizen hazard reports.
    """
    reports = await report_service.get_all_reports(status=status, severity=severity, state=state)
    return {"total": len(reports), "reports": reports}


@router.delete("/reports/{report_id}")
async def delete_hazard_report(report_id: str):
    """
    Delete a field hazard report from database.
    """
    import database
    if database._pool is None:
        raise HTTPException(status_code=503, detail="Database service unavailable")

    with database.get_db() as cur:
        cur.execute("SELECT id FROM hazard_reports WHERE id = %s", (report_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Hazard report not found")

        cur.execute("DELETE FROM hazard_reports WHERE id = %s", (report_id,))
        cur.execute("DELETE FROM report_audit_logs WHERE report_id = %s", (report_id,))

    return {"success": True, "message": f"Report {report_id} deleted successfully."}


@router.patch("/reports/{report_id}/status")
async def update_report_status(
    report_id: str,
    update: HazardReportStatusUpdate,
    user: dict = Depends(require_roles(["FIELD_WORKER", "AUTHORITY", "ADMIN"]))
):
    """
    Disaster governance action: Update report status (Authority / Field Worker only).
    """
    res = await report_service.update_report_status(report_id, update, user)
    if not res.get("success"):
        raise HTTPException(status_code=404, detail=res.get("message"))
    return res
