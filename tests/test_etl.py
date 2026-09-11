import os
import pandas as pd
import pytest
from etl.extract import extract_data
from etl.transform import transform_data
from etl.validate import validate_data
from etl.pipeline import run_etl_pipeline

def test_extract_module():
    datasets = extract_data()
    assert "customers" in datasets
    assert "products" in datasets
    assert "orders" in datasets
    assert "order_items" in datasets

def test_transform_financial_calculations():
    # Mock orders and items
    df_orders = pd.DataFrame([{
        "order_id": "ORD-0000001",
        "order_date": "2024-01-15",
        "customer_id": 1,
        "region_id": 1,
        "employee_id": 1
    }])

    df_items = pd.DataFrame([{
        "order_id": "ORD-0000001",
        "product_id": 10,
        "quantity": 2,
        "unit_price": 100.0,
        "unit_cost": 60.0,
        "discount": 0.10
    }])

    df_products = pd.DataFrame([{
        "product_id": 10,
        "sku": "SKU-001",
        "product_name": "Test Product",
        "category": "Tech",
        "subcategory": "Gadgets",
        "unit_cost": 60.0,
        "unit_price": 100.0
    }])

    raw = {"orders": df_orders, "order_items": df_items, "products": df_products}
    transformed = transform_data(raw)
    
    assert "fact_sales" in transformed
    df_sales = transformed["fact_sales"]
    assert len(df_sales) == 1
    
    # 2 * 100 * (1 - 0.10) = 180.0
    assert float(df_sales["revenue"].iloc[0]) == 180.0
    # 2 * 60 = 120.0
    assert float(df_sales["cost"].iloc[0]) == 120.0
    # 180 - 120 = 60.0
    assert float(df_sales["profit"].iloc[0]) == 60.0

def test_data_validation_rules():
    df_sales = pd.DataFrame([
        # Valid row
        {"order_id": "O1", "product_id": 1, "customer_id": 1, "date_id": 20240101, "quantity": 5, "revenue": 100.0},
        # Invalid row: negative quantity
        {"order_id": "O2", "product_id": 2, "customer_id": 1, "date_id": 20240101, "quantity": -1, "revenue": 50.0},
        # Invalid row: duplicate
        {"order_id": "O1", "product_id": 1, "customer_id": 1, "date_id": 20240101, "quantity": 5, "revenue": 100.0}
    ])

    raw = {"fact_sales": df_sales}
    validated, report = validate_data(raw)
    
    assert "fact_sales" in validated
    assert len(validated["fact_sales"]) == 1
    assert report["duplicates_removed"] == 1
    assert report["invalid_rows"] > 0

def test_full_pipeline_run():
    result = run_etl_pipeline()
    assert result["success"] is True
    assert result["quality_report"]["quality_score_percent"] >= 95.0
