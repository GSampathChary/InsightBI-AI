"""
InsightBI AI — Product Endpoints (backend/app/api/v1/products.py)
"""

from fastapi import APIRouter
from backend.app.services.analytics_service import get_analytics_summary

router = APIRouter()

@router.get("/top")
def get_top_products():
    summary = get_analytics_summary()
    return summary.get("top_products", [])

@router.get("/catalog")
def get_product_catalog():
    summary = get_analytics_summary()
    return {"products": summary.get("top_products", [])}
