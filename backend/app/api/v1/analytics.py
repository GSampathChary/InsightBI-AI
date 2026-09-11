"""
InsightBI AI — Analytics & ML Endpoints (backend/app/api/v1/analytics.py)
"""

import os
import pandas as pd
from fastapi import APIRouter
from backend.app.services.analytics_service import get_analytics_summary

router = APIRouter()

SAMPLE_FORECAST = [
    {"ds": "2024-07-01", "yhat": 265000.0, "yhat_lower": 245000.0, "yhat_upper": 285000.0, "territory": "Overall"},
    {"ds": "2024-08-01", "yhat": 278000.0, "yhat_lower": 258000.0, "yhat_upper": 298000.0, "territory": "Overall"},
    {"ds": "2024-09-01", "yhat": 295000.0, "yhat_lower": 272000.0, "yhat_upper": 318000.0, "territory": "Overall"},
    {"ds": "2024-10-01", "yhat": 310000.0, "yhat_lower": 285000.0, "yhat_upper": 335000.0, "territory": "Overall"},
    {"ds": "2024-11-01", "yhat": 385000.0, "yhat_lower": 350000.0, "yhat_upper": 420000.0, "territory": "Overall"},
    {"ds": "2024-12-01", "yhat": 425000.0, "yhat_lower": 390000.0, "yhat_upper": 460000.0, "territory": "Overall"}
]

SAMPLE_ANOMALIES = [
    {"sales_id": 1402, "order_id": "ORD-0001402", "date": "2024-04-12", "revenue": 45000.0, "anomaly_score": -0.42, "reason": "Unusual bulk order volume spiking 450% above baseline"},
    {"sales_id": 2891, "order_id": "ORD-0002891", "date": "2024-05-28", "revenue": 62000.0, "anomaly_score": -0.58, "reason": "High single-transaction value for Enterprise Cloud License"}
]

@router.get("/forecast")
def get_sales_forecast():
    filepath = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data", "processed", "forecast_predictions.csv")
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            if not df.empty:
                return df.to_dict(orient="records")
        except Exception:
            pass
    return SAMPLE_FORECAST

@router.get("/anomalies")
def get_sales_anomalies():
    filepath = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data", "processed", "sales_anomalies.csv")
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            if not df.empty:
                return df.to_dict(orient="records")
        except Exception:
            pass
    return SAMPLE_ANOMALIES

@router.get("/insights")
def get_business_insights():
    summary = get_analytics_summary()
    return summary.get("business_insights", [])
