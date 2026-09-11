"""
InsightBI AI — Scheduled Reporting Service (analytics/reporting/scheduler.py)
Manages automated daily/weekly report generation tasks.
"""

import logging
from typing import Dict, Any
from analytics.reporting.pdf_exporter import export_executive_pdf
from analytics.reporting.csv_exporter import export_summary_csv

logger = logging.getLogger("insightbi.reporting.scheduler")

class ReportScheduler:
    def __init__(self):
        self.schedules = []

    def schedule_report(self, report_type: str, frequency: str, recipient_email: str) -> Dict[str, Any]:
        """Schedules automated report dispatch."""
        job = {
            "job_id": len(self.schedules) + 1,
            "report_type": report_type,
            "frequency": frequency,
            "recipient_email": recipient_email,
            "status": "Active"
        }
        self.schedules.append(job)
        logger.info(f"Scheduled report job #{job['job_id']} ({frequency}) for {recipient_email}")
        return job

    def run_pending_jobs(self) -> Dict[str, Any]:
        """Executes all pending scheduled report jobs."""
        pdf_path = export_executive_pdf()
        csv_files = export_summary_csv()
        return {
            "jobs_executed": len(self.schedules),
            "generated_pdf": pdf_path,
            "generated_csv_bundle": csv_files
        }

def get_scheduler() -> ReportScheduler:
    return ReportScheduler()
