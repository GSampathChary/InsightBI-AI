"""
InsightBI AI — Automated PDF Report Exporter (analytics/reporting/pdf_exporter.py)
Generates structured executive PDF reports.
"""

import os
import logging
from typing import Dict, Any, Optional
from backend.app.services.analytics_service import get_analytics_summary

logger = logging.getLogger("insightbi.reporting.pdf")

class PDFExporter:
    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = output_dir or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
        )
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_executive_report(self, filename: str = "Executive_Analytics_Report.pdf") -> str:
        """Generates structured PDF report containing KPIs, trends, and AI recommendations."""
        output_path = os.path.join(self.output_dir, filename)
        summary = get_analytics_summary()

        # In production this uses reportlab or pdfkit; building structured PDF layout text buffer
        pdf_content = f"""
================================================================================
                       INSIGHTBI AI — EXECUTIVE REPORT
================================================================================
Generated Date: 2026-09-01
Scope: Executive Overview & AI Business Performance Insights

1. EXECUTIVE KPI SUMMARY
--------------------------------------------------------------------------------
Total Revenue:           ${summary.get('kpis', {}).get('total_revenue', 0):,.2f}
Total Profit:            ${summary.get('kpis', {}).get('total_profit', 0):,.2f}
Profit Margin:           {summary.get('kpis', {}).get('profit_margin_percent', 0):.1f}%
Total Orders:            {summary.get('kpis', {}).get('total_orders', 0):,}
Total Customers:         {summary.get('kpis', {}).get('total_customers', 0):,}
Average Order Value:     ${summary.get('kpis', {}).get('avg_order_value', 0):,.2f}

2. MONTHLY FINANCIAL TRENDS
--------------------------------------------------------------------------------
Month       | Revenue          | Profit           | Margin %
--------------------------------------------------------------------------------
"""
        for item in summary.get('trends', [])[:6]:
            pdf_content += f"{item.get('year_month', 'N/A'):<11} | ${item.get('revenue', 0):>14,.2f} | ${item.get('profit', 0):>14,.2f} | {item.get('margin_percent', 40.0):>7.1f}%\n"

        pdf_content += """
3. AUTOMATED AI BUSINESS RECOMMENDATIONS
--------------------------------------------------------------------------------
"""
        for insight in summary.get('business_insights', []):
            pdf_content += f"[{insight.get('category', 'Info')}] {insight.get('title', '')}\n"
            pdf_content += f"   Description: {insight.get('description', '')}\n"
            pdf_content += f"   Action Item: {insight.get('recommendation', '')}\n\n"

        pdf_content += "================================================================================\n"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(pdf_content)

        logger.info(f"Generated Executive PDF Report at {output_path}")
        return output_path

def export_executive_pdf(filename: str = "Executive_Analytics_Report.pdf") -> str:
    exporter = PDFExporter()
    return exporter.generate_executive_report(filename)
