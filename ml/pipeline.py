"""
InsightBI AI — Unified ML Pipeline Orchestrator (ml/pipeline.py)
Executes Sales Forecasting, RFM Customer Segmentation, and Anomaly Detection models.
Persists outputs to data/processed/ and database tables.
"""

import os
import logging
import pandas as pd
from typing import Dict, Any
from ml.forecasting.train_forecaster import train_sales_forecaster
from ml.segmentation.cluster_customers import train_customer_segmentation
from ml.anomalies.detect_anomalies import detect_sales_anomalies

logger = logging.getLogger("insightbi.ml.pipeline")

class MLPipeline:
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
        else:
            self.data_dir = data_dir

    def run((self)) -> Dict[str, Any]:
        logger.info("=" * 60)
        logger.info("Starting InsightBI AI Machine Learning Pipeline Execution...")
        logger.info("=" * 60)

        sales_path = os.path.join(self.data_dir, "sales_clean.csv")
        customers_path = os.path.join(self.data_dir, "customers_clean.csv")

        if not os.path.exists(sales_path):
            logger.error(f"Clean sales file not found at {sales_path}. Run ETL pipeline first.")
            return {"success": False, "error": "Clean sales file missing"}

        df_sales = pd.read_csv(sales_path)
        df_customers = pd.read_csv(customers_path) if os.path.exists(customers_path) else None

        # 1. Sales Forecasting
        logger.info("[ML 1/3] Training Sales Forecasting Model (90-day horizon)...")
        forecast_res = train_sales_forecaster(df_sales, forecast_days=90)
        df_forecast = pd.DataFrame(forecast_res.get("forecast", []))
        if not df_forecast.empty:
            df_forecast.to_csv(os.path.join(self.data_dir, "forecast_predictions.csv"), index=False)
            logger.info(f"Saved {len(df_forecast)} forecast predictions to data/processed/forecast_predictions.csv")

        # 2. Customer RFM Segmentation
        logger.info("[ML 2/3] Computing RFM Scores & K-Means Customer Clustering...")
        df_segments = train_customer_segmentation(df_sales, df_customers)
        if not df_segments.empty:
            df_segments.to_csv(os.path.join(self.data_dir, "customer_segments.csv"), index=False)
            logger.info(f"Saved {len(df_segments):,} customer RFM segments to data/processed/customer_segments.csv")

        # 3. Revenue Anomaly Detection
        logger.info("[ML 3/3] Running Isolation Forest Anomaly Detector...")
        df_anomalies = detect_sales_anomalies(df_sales)
        if not df_anomalies.empty:
            df_anomalies.to_csv(os.path.join(self.data_dir, "sales_anomalies.csv"), index=False)
            logger.info(f"Saved {len(df_anomalies)} sales anomalies to data/processed/sales_anomalies.csv")

        logger.info("=" * 60)
        logger.info("ML Pipeline Execution Completed Successfully!")
        logger.info("=" * 60)

        return {
            "success": True,
            "forecast_count": len(df_forecast),
            "segments_count": len(df_segments),
            "anomalies_count": len(df_anomalies),
            "forecast_metrics": forecast_res.get("metrics", {})
        }

def run_ml_pipeline(data_dir: str = None) -> Dict[str, Any]:
    pipeline = MLPipeline(data_dir=data_dir)
    return pipeline.run()
