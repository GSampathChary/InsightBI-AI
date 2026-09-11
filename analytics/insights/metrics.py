"""
InsightBI AI — Analytics Engine: Metrics (analytics/insights/metrics.py)
Reusable analytical metrics functions computing Revenue, Profit, AOV, Margin %, Growth %, Retention.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List

def compute_overall_kpis(df_sales: pd.DataFrame, df_customers: pd.DataFrame = None) -> Dict[str, Any]:
    """Computes high-level executive KPIs."""
    if df_sales.empty:
        return {
            "total_revenue": 0.0,
            "total_profit": 0.0,
            "total_orders": 0,
            "total_customers": 0,
            "avg_order_value": 0.0,
            "profit_margin_percent": 0.0
        }

    total_revenue = float(df_sales["revenue"].sum())
    total_profit = float(df_sales["profit"].sum())
    total_orders = int(df_sales["order_id"].nunique())
    
    if "customer_id" in df_sales.columns:
        total_customers = int(df_sales["customer_id"].nunique())
    elif df_customers is not None and not df_customers.empty:
        total_customers = len(df_customers)
    else:
        total_customers = 0

    avg_order_value = round(total_revenue / total_orders, 2) if total_orders > 0 else 0.0
    profit_margin = round((total_profit / total_revenue) * 100.0, 2) if total_revenue > 0 else 0.0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "total_orders": total_orders,
        "total_customers": total_customers,
        "avg_order_value": avg_order_value,
        "profit_margin_percent": profit_margin
    }

def compute_sales_trends(df_sales: pd.DataFrame) -> List[Dict[str, Any]]:
    """Computes monthly sales trends, revenue, profit, and Month-over-Month (MoM) growth %."""
    if df_sales.empty:
        return []

    df = df_sales.copy()
    if "date" in df.columns:
        df["year_month"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m")
    elif "date_id" in df.columns:
        df["year_month"] = df["date_id"].astype(str).str.slice(0, 6).apply(lambda s: f"{s[:4]}-{s[4:6]}")
    else:
        return []

    monthly = df.groupby("year_month").agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        customers=("customer_id", "nunique")
    ).reset_index().sort_values("year_month")

    # MoM & YoY Growth Calculations
    monthly["mom_growth_percent"] = monthly["revenue"].pct_change() * 100.0
    monthly["mom_growth_percent"] = monthly["mom_growth_percent"].fillna(0.0).round(2)

    results = []
    for _, row in monthly.iterrows():
        results.append({
            "year_month": row["year_month"],
            "revenue": round(float(row["revenue"]), 2),
            "profit": round(float(row["profit"]), 2),
            "orders": int(row["orders"]),
            "customers": int(row["customers"]),
            "mom_growth_percent": float(row["mom_growth_percent"])
        })
    return results

def compute_product_performance(df_sales: pd.DataFrame, df_products: pd.DataFrame = None, top_n: int = 10) -> Dict[str, List[Dict[str, Any]]]:
    """Returns top N and bottom N products by revenue and profit margin."""
    if df_sales.empty:
        return {"top_products": [], "bottom_products": []}

    df = df_sales.copy()
    grouped = df.groupby("product_id").agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        quantity_sold=("quantity", "sum"),
        order_count=("order_id", "nunique")
    ).reset_index()

    if df_products is not None and not df_products.empty:
        grouped = pd.merge(grouped, df_products[["product_id", "product_name", "category"]], on="product_id", how="left")
    else:
        grouped["product_name"] = grouped["product_id"].apply(lambda p: f"Product #{p}")
        grouped["category"] = "General"

    grouped["profit_margin_percent"] = (grouped["profit"] / grouped["revenue"] * 100.0).fillna(0.0).round(2)
    grouped = grouped.sort_values("revenue", ascending=False)

    top_prods = grouped.head(top_n).to_dict(orient="records")
    bottom_prods = grouped.tail(top_n).sort_values("revenue", ascending=True).to_dict(orient="records")

    return {
        "top_products": top_prods,
        "bottom_products": bottom_prods
    }

def compute_regional_performance(df_sales: pd.DataFrame, df_regions: pd.DataFrame = None) -> List[Dict[str, Any]]:
    """Computes regional performance breakdowns."""
    if df_sales.empty:
        return []

    df = df_sales.copy()
    grouped = df.groupby("region_id").agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        customers=("customer_id", "nunique")
    ).reset_index()

    if df_regions is not None and not df_regions.empty:
        grouped = pd.merge(grouped, df_regions[["region_id", "region_name", "state"]], on="region_id", how="left")
    else:
        grouped["region_name"] = grouped["region_id"].apply(lambda r: f"Region #{r}")
        grouped["state"] = "N/A"

    grouped["profit_margin_percent"] = (grouped["profit"] / grouped["revenue"] * 100.0).fillna(0.0).round(2)
    return grouped.sort_values("revenue", ascending=False).to_dict(orient="records")
