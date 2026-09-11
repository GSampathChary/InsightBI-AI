"""
InsightBI AI — Sales Endpoints (backend/app/api/v1/sales.py)
"""

from fastapi import APIRouter
from backend.app.services.analytics_service import get_analytics_summary

router = APIRouter()

@router.get("/overview")
def get_sales_overview():
    summary = get_analytics_summary()
    return {
        "kpis": summary.get("kpis", {}),
        "trends": summary.get("trends", [])
    }

@router.get("/regional")
def get_regional_sales():
    summary = get_analytics_summary()
    return summary.get("regional_performance", [])
