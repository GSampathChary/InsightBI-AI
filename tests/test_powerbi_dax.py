import pandas as pd
import pytest
from analytics.insights.metrics import compute_overall_kpis

def test_dax_formula_equivalents():
    """Validates DAX formula math against Python Pandas reference calculations."""
    df_sales = pd.DataFrame([
        {"order_id": "ORD-1", "customer_id": 1, "revenue": 1000.0, "cost": 600.0, "profit": 400.0, "quantity": 5},
        {"order_id": "ORD-2", "customer_id": 2, "revenue": 2000.0, "cost": 1200.0, "profit": 800.0, "quantity": 10},
        {"order_id": "ORD-3", "customer_id": 1, "revenue": 1500.0, "cost": 900.0, "profit": 600.0, "quantity": 8}
    ])

    # DAX: Total Revenue = SUM(fact_sales[revenue])
    dax_total_revenue = float(df_sales["revenue"].sum())
    assert dax_total_revenue == 4500.0

    # DAX: Total Profit = SUM(fact_sales[profit])
    dax_total_profit = float(df_sales["profit"].sum())
    assert dax_total_profit == 1800.0

    # DAX: Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)
    dax_profit_margin = round((dax_total_profit / dax_total_revenue) * 100.0, 2)
    assert dax_profit_margin == 40.0

    # DAX: Total Orders = DISTINCTCOUNT(fact_sales[order_id])
    dax_total_orders = int(df_sales["order_id"].nunique())
    assert dax_total_orders == 3

    # DAX: Total Customers = DISTINCTCOUNT(fact_sales[customer_id])
    dax_total_customers = int(df_sales["customer_id"].nunique())
    assert dax_total_customers == 2

    # DAX: AOV = DIVIDE([Total Revenue], [Total Orders], 0)
    dax_aov = round(dax_total_revenue / dax_total_orders, 2)
    assert dax_aov == 1500.0

    # DAX: Repeat Customer Count = CALCULATE([Total Customers], FILTER(dim_customer, [Total Orders] > 1))
    cust_orders = df_sales.groupby("customer_id")["order_id"].nunique()
    dax_repeat_cust = int((cust_orders > 1).sum())
    assert dax_repeat_cust == 1
