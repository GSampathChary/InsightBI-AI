import os
import pytest
from fastapi.testclient import TestClient
from analytics.reporting.pdf_exporter import export_executive_pdf
from analytics.reporting.csv_exporter import export_summary_csv
from analytics.reporting.scheduler import get_scheduler
from backend.app.main import app

client = TestClient(app)

def test_pdf_exporter():
    pdf_path = export_executive_pdf("test_report.pdf")
    assert os.path.exists(pdf_path)
    assert os.path.getsize(pdf_path) > 0

def test_csv_exporter():
    bundle = export_summary_csv()
    assert "trends" in bundle
    assert os.path.exists(bundle["trends"])

def test_report_scheduler():
    scheduler = get_scheduler()
    job = scheduler.schedule_report("Executive Overview", "Daily", "ceo@insightbi.ai")
    assert job["job_id"] > 0
    assert job["recipient_email"] == "ceo@insightbi.ai"

    results = scheduler.run_pending_jobs()
    assert results["jobs_executed"] > 0

def test_reports_api_endpoints():
    res_csv = client.get("/api/v1/reports/csv")
    assert res_csv.status_code == 200
    assert "files" in res_csv.json()

    res_sched = client.post("/api/v1/reports/schedule", json={
        "report_type": "Executive Summary",
        "frequency": "Weekly",
        "recipient_email": "cfo@insightbi.ai"
    })
    assert res_sched.status_code == 200
    assert res_sched.json()["job"]["recipient_email"] == "cfo@insightbi.ai"
