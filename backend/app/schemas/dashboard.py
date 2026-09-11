"""
InsightBI AI — Dashboard Schemas (backend/app/schemas/dashboard.py)
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class KPIMetrics(BaseModel):
    total_revenue: float
    total_profit: float
    total_orders: int
    total_customers: int
    avg_order_value: float
    profit_margin_percent: float

class TrendItem(BaseModel):
    year_month: str
    revenue: float
    profit: float
    orders: int
    customers: int
    mom_growth_percent: float

class DashboardSummaryResponse(BaseModel):
    kpis: KPIMetrics
    trends: List[TrendItem]
    top_products: List[Dict[str, Any]]
    regional_performance: List[Dict[str, Any]]
    business_insights: List[Dict[str, Any]]
