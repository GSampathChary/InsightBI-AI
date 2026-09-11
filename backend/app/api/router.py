"""
InsightBI AI — Main API Router (backend/app/api/router.py)
"""

from fastapi import APIRouter
from backend.app.api.v1 import auth, dashboard, sales, products, customers, analytics, copilot, reports, upload

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(sales.router, prefix="/sales", tags=["sales"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(copilot.router, prefix="/copilot", tags=["copilot"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
