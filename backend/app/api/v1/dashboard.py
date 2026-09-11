"""
InsightBI AI — Dashboard Endpoints (backend/app/api/v1/dashboard.py)
"""

from fastapi import APIRouter
from backend.app.services.analytics_service import get_analytics_summary

router = APIRouter()

@router.get("/summary")
def get_dashboard_summary():
    """Returns complete executive dashboard metrics, trends, products, and insights."""
    return get_analytics_summary()

@router.get("/kpis")
def get_dashboard_kpis():
    """Returns high-level executive KPIs."""
    summary = get_analytics_summary()
    return summary.get("kpis", {})

@router.get("/trends")
def get_dashboard_trends():
    """Returns monthly sales trends."""
    summary = get_analytics_summary()
    return summary.get("trends", [])

@router.get("/dataset")
def get_dataset_details():
    """Small operational payload for data freshness and volume indicators."""
    return get_analytics_summary().get("dataset", {})
