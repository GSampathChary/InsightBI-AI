import pandas as pd
import pytest
from analytics.insights.metrics import compute_overall_kpis, compute_sales_trends, compute_product_performance, compute_regional_performance
from analytics.insights.business_insights import generate_automated_insights
from backend.app.services.analytics_service import AnalyticsService

def test_compute_overall_kpis():
    df_sales = pd.DataFrame([
        {"order_id": "O1", "customer_id": 1, "revenue": 100.0, "profit": 40.0},
        {"order_id": "O2", "customer_id": 2, "revenue": 200.0, "profit": 100.0}
    ])
    kpis = compute_overall_kpis(df_sales)
    assert kpis["total_revenue"] == 300.0
    assert kpis["total_profit"] == 140.0
    assert kpis["total_orders"] == 2
    assert kpis["total_customers"] == 2
    assert kpis["avg_order_value"] == 150.0
    assert kpis["profit_margin_percent"] == 46.67

def test_compute_sales_trends():
    df_sales = pd.DataFrame([
        {"date_id": 20240115, "order_id": "O1", "customer_id": 1, "revenue": 100.0, "profit": 40.0},
        {"date_id": 20240215, "order_id": "O2", "customer_id": 1, "revenue": 200.0, "profit": 90.0}
    ])
    trends = compute_sales_trends(df_sales)
    assert len(trends) == 2
    assert trends[0]["year_month"] == "2024-01"
    assert trends[1]["year_month"] == "2024-02"
    assert trends[1]["mom_growth_percent"] == 100.0

def test_business_insights_generation():
    df_sales = pd.DataFrame([
        {"order_id": "O1", "customer_id": 1, "product_id": 10, "region_id": 1, "revenue": 1000.0, "profit": 500.0},
        {"order_id": "O2", "customer_id": 1, "product_id": 10, "region_id": 1, "revenue": 1000.0, "profit": 500.0}
    ])
    insights = generate_automated_insights(df_sales)
    assert len(insights) >= 2
    categories = [ins["category"] for ins in insights]
    assert "Growth" in categories or "Customer" in categories

def test_analytics_service_summary():
    service = AnalyticsService()
    summary = service.get_dashboard_summary()
    assert "kpis" in summary
    assert "trends" in summary
    assert "business_insights" in summary
