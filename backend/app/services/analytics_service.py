"""
InsightBI AI — Backend Analytics Service (backend/app/services/analytics_service.py)
Wraps analytics metrics functions and loads analytical datasets from data/processed/ or PostgreSQL.
Provides rich fallback metrics if files are empty/missing.
"""

import os
import time
import pandas as pd
from typing import Dict, Any, List
from analytics.insights.metrics import compute_overall_kpis, compute_sales_trends, compute_product_performance, compute_regional_performance
from analytics.insights.business_insights import generate_automated_insights

SAMPLE_KPIS = {
    "total_revenue": 2458900.50,
    "total_profit": 892400.25,
    "total_orders": 12450,
    "total_customers": 8420,
    "avg_order_value": 197.50,
    "profit_margin_percent": 36.29
}

SAMPLE_TRENDS = [
    {"year_month": "2024-01", "revenue": 185000.0, "profit": 64750.0, "orders": 930, "customers": 810, "mom_growth_percent": 0.0},
    {"year_month": "2024-02", "revenue": 198000.0, "profit": 71280.0, "orders": 995, "customers": 845, "mom_growth_percent": 7.03},
    {"year_month": "2024-03", "revenue": 215000.0, "profit": 77400.0, "orders": 1080, "customers": 910, "mom_growth_percent": 8.59},
    {"year_month": "2024-04", "revenue": 210000.0, "profit": 75600.0, "orders": 1050, "customers": 890, "mom_growth_percent": -2.33},
    {"year_month": "2024-05", "revenue": 235000.0, "profit": 86950.0, "orders": 1180, "customers": 980, "mom_growth_percent": 11.90},
    {"year_month": "2024-06", "revenue": 258000.0, "profit": 95460.0, "orders": 1290, "customers": 1050, "mom_growth_percent": 9.79}
]

SAMPLE_PRODUCTS = [
    {"product_id": 101, "product_name": "Enterprise Laptop Pro 15", "category": "Technology", "revenue": 485000.0, "profit": 169750.0, "quantity_sold": 410, "profit_margin_percent": 35.0},
    {"product_id": 102, "product_name": "UltraWide Monitor 34-Inch", "category": "Technology", "revenue": 342000.0, "profit": 136800.0, "quantity_sold": 570, "profit_margin_percent": 40.0},
    {"product_id": 103, "product_name": "Ergonomic Office Chair", "category": "Furniture", "revenue": 289000.0, "profit": 121380.0, "quantity_sold": 820, "profit_margin_percent": 42.0},
    {"product_id": 104, "product_name": "Standing Desk Electric", "category": "Furniture", "revenue": 245000.0, "profit": 93100.0, "quantity_sold": 350, "profit_margin_percent": 38.0},
    {"product_id": 105, "product_name": "Cloud License Enterprise", "category": "Software", "revenue": 198000.0, "profit": 158400.0, "quantity_sold": 990, "profit_margin_percent": 80.0}
]

SAMPLE_REGIONS = [
    {"region_id": 1, "region_name": "North India", "state": "Delhi NCR", "revenue": 780000.0, "profit": 288600.0, "orders": 3900, "customers": 2600, "profit_margin_percent": 37.0},
    {"region_id": 2, "region_name": "West India", "state": "Maharashtra", "revenue": 690000.0, "profit": 255300.0, "orders": 3450, "customers": 2300, "profit_margin_percent": 37.0},
    {"region_id": 3, "region_name": "South India", "state": "Karnataka", "revenue": 540000.0, "profit": 189000.0, "orders": 2700, "customers": 1800, "profit_margin_percent": 35.0},
    {"region_id": 4, "region_name": "East India", "state": "West Bengal", "revenue": 448900.5, "profit": 159500.25, "orders": 2400, "customers": 1720, "profit_margin_percent": 35.53}
]

SAMPLE_INSIGHTS = [
    {"category": "Sales", "title": "Revenue Growth Spike in Q2", "narrative": "Q2 sales grew by 11.9% MoM driven primarily by Technology category demand.", "impact": "High", "action": "Increase inventory buffer for top-selling Enterprise Laptops."},
    {"category": "Customers", "title": "VIP Segment Retention", "narrative": "VIP customers account for 48% of total revenue despite making up 15% of customer base.", "impact": "High", "action": "Deploy dedicated account management for VIP tier."},
    {"category": "Products", "title": "High Margin Software Subscriptions", "narrative": "SaaS subscriptions achieved an 80% gross profit margin.", "impact": "Medium", "action": "Promote annual recurring subscription bundles."}
]

class AnalyticsService:
    # Dashboard pages request the same aggregates repeatedly. Cache the compact
    # report bundle and invalidate it only when a processed dataset changes.
    _summary_cache: Dict[str, Any] = {}
    _cache_signature: tuple = ()
    _cache_created_at: float = 0.0
    CACHE_TTL_SECONDS = 60

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "processed")
        else:
            self.data_dir = data_dir

    def _load_dataset(self, filename: str) -> pd.DataFrame:
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                if not df.empty:
                    return df
            except Exception:
                pass
        return pd.DataFrame()

    def _dataset_signature(self) -> tuple:
        """A cheap change detector; avoids re-reading large files per request."""
        filenames = ("sales_clean.csv", "customers_clean.csv", "products_clean.csv")
        return tuple(
            (filename, os.path.getmtime(os.path.join(self.data_dir, filename)), os.path.getsize(os.path.join(self.data_dir, filename)))
            if os.path.exists(os.path.join(self.data_dir, filename)) else (filename, 0, 0)
            for filename in filenames
        )

    def get_dataset_metadata(self) -> Dict[str, Any]:
        sales_path = os.path.join(self.data_dir, "sales_clean.csv")
        if not os.path.exists(sales_path):
            return {"source": "sample data", "row_count": 0, "storage": "demo", "refresh_mode": "on demand"}
        try:
            # Counting lines is memory-safe even for very large CSV exports.
            with open(sales_path, "rb") as source:
                row_count = max(sum(1 for _ in source) - 1, 0)
            return {
                "source": "uploaded dataset",
                "row_count": row_count,
                "storage": "aggregated reporting model",
                "refresh_mode": "cached for 60 seconds",
                "file_size_mb": round(os.path.getsize(sales_path) / (1024 * 1024), 2),
                "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(os.path.getmtime(sales_path)))
            }
        except OSError:
            return {"source": "uploaded dataset", "row_count": 0, "storage": "aggregated reporting model", "refresh_mode": "cached for 60 seconds"}

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Provides complete analytics bundle for frontend dashboards."""
        signature = self._dataset_signature()
        if (AnalyticsService._summary_cache and signature == AnalyticsService._cache_signature
                and time.time() - AnalyticsService._cache_created_at < self.CACHE_TTL_SECONDS):
            return AnalyticsService._summary_cache

        df_sales = self._load_dataset("sales_clean.csv")
        df_customers = self._load_dataset("customers_clean.csv")
        df_products = self._load_dataset("products_clean.csv")

        if df_sales.empty:
            result = {
                "kpis": SAMPLE_KPIS,
                "trends": SAMPLE_TRENDS,
                "top_products": SAMPLE_PRODUCTS,
                "regional_performance": SAMPLE_REGIONS,
                "business_insights": SAMPLE_INSIGHTS
            }
            result["dataset"] = self.get_dataset_metadata()
            AnalyticsService._summary_cache, AnalyticsService._cache_signature, AnalyticsService._cache_created_at = result, signature, time.time()
            return result

        kpis = compute_overall_kpis(df_sales, df_customers)
        trends = compute_sales_trends(df_sales)
        products = compute_product_performance(df_sales, df_products, top_n=5)
        regions = compute_regional_performance(df_sales)
        insights = generate_automated_insights(df_sales, df_customers, df_products)

        result = {
            "kpis": kpis if kpis.get("total_revenue", 0) > 0 else SAMPLE_KPIS,
            "trends": trends if len(trends) > 0 else SAMPLE_TRENDS,
            "top_products": products.get("top_products", []) if len(products.get("top_products", [])) > 0 else SAMPLE_PRODUCTS,
            "regional_performance": regions if len(regions) > 0 else SAMPLE_REGIONS,
            "business_insights": insights if len(insights) > 0 else SAMPLE_INSIGHTS
        }
        result["dataset"] = self.get_dataset_metadata()
        AnalyticsService._summary_cache, AnalyticsService._cache_signature, AnalyticsService._cache_created_at = result, signature, time.time()
        return result

def get_analytics_summary() -> Dict[str, Any]:
    service = AnalyticsService()
    return service.get_dashboard_summary()
