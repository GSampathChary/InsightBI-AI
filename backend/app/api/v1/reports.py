"""
InsightBI AI — Reports REST Endpoints (backend/app/api/v1/reports.py)
"""

from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from analytics.reporting.pdf_exporter import export_executive_pdf
from analytics.reporting.csv_exporter import export_summary_csv
from analytics.reporting.scheduler import get_scheduler

router = APIRouter()

class ScheduleReportRequest(BaseModel):
    report_type: str = "Executive PDF"
    frequency: str = "Weekly"
    recipient_email: str

@router.get("/pdf")
def get_pdf_report():
    pdf_path = export_executive_pdf()
    return FileResponse(pdf_path, filename="Executive_Analytics_Report.pdf", media_type="application/pdf")

@router.get("/csv")
def get_csv_reports():
    bundle = export_summary_csv()
    return {"message": "CSV reporting bundle generated", "files": bundle}

@router.post("/schedule")
def schedule_report(request: ScheduleReportRequest):
    scheduler = get_scheduler()
    job = scheduler.schedule_report(request.report_type, request.frequency, request.recipient_email)
    return {"message": "Report schedule created", "job": job}
