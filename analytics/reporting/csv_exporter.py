"""
InsightBI AI — Automated CSV Report Exporter (analytics/reporting/csv_exporter.py)
"""

import os
import pandas as pd
import logging
from typing import Dict, Any, Optional
from backend.app.services.analytics_service import get_analytics_summary

logger = logging.getLogger("insightbi.reporting.csv")

class CSVExporter:
    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = output_dir or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
        )
        os.makedirs(self.output_dir, exist_ok=True)

    def export_summary_bundle(self) -> Dict[str, str]:
        """Exports clean CSV files for trends, products, regional performance, and insights."""
        summary = get_analytics_summary()
        exported_files = {}

        # 1. Trends CSV
        trends_df = pd.DataFrame(summary.get("trends", []))
        trends_path = os.path.join(self.output_dir, "report_sales_trends.csv")
        trends_df.to_csv(trends_path, index=False)
        exported_files["trends"] = trends_path

        # 2. Top Products CSV
        products_df = pd.DataFrame(summary.get("top_products", []))
        products_path = os.path.join(self.output_dir, "report_top_products.csv")
        products_df.to_csv(products_path, index=False)
        exported_files["products"] = products_path

        # 3. Regional Performance CSV
        regional_df = pd.DataFrame(summary.get("regional_performance", []))
        regional_path = os.path.join(self.output_dir, "report_regional_performance.csv")
        regional_df.to_csv(regional_path, index=False)
        exported_files["regional"] = regional_path

        logger.info(f"Exported CSV Summary Bundle to {self.output_dir}")
        return exported_files

def export_summary_csv() -> Dict[str, str]:
    exporter = CSVExporter()
    return exporter.export_summary_bundle()
