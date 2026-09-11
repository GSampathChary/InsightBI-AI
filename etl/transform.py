"""
InsightBI AI — ETL Module: Transform (etl/transform.py)
Transforms, normalizes, and calculates business metrics for extracted raw datasets.
Calculates revenue, cost, profit, and date_id mappings.
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime

logger = logging.getLogger("insightbi.etl.transform")

class DataTransformer:

    def transform_regions(self, df_regions: pd.DataFrame) -> pd.DataFrame:
        """Transforms region dimension."""
        if df_regions.empty:
            return df_regions
        df = df_regions.copy()
        df["region_name"] = df["region_name"].astype(str).str.strip()
        df["state"] = df["state"].astype(str).str.strip()
        df["country"] = df["country"].fillna("United States").astype(str).str.strip()
        return df

    def transform_customers(self, df_customers: pd.DataFrame) -> pd.DataFrame:
        """Transforms customer dimension data."""
        if df_customers.empty:
            return df_customers
        df = df_customers.copy()
        df["first_name"] = df["first_name"].astype(str).str.strip().str.title()
        df["last_name"] = df["last_name"].astype(str).str.strip().str.title()
        df["email"] = df["email"].astype(str).str.strip().str.lower()
        df["registration_date"] = pd.to_datetime(df["registration_date"], errors="coerce").dt.strftime("%Y-%m-%d")
        df["customer_segment"] = df["customer_segment"].fillna("Standard").astype(str).str.strip()
        df["credit_limit"] = pd.to_numeric(df["credit_limit"], errors="coerce").fillna(1000.0)
        return df

    def transform_products(self, df_products: pd.DataFrame) -> pd.DataFrame:
        """Transforms product catalog dimension."""
        if df_products.empty:
            return df_products
        df = df_products.copy()
        df["sku"] = df["sku"].astype(str).str.strip().str.upper()
        df["product_name"] = df["product_name"].astype(str).str.strip()
        df["category"] = df["category"].astype(str).str.strip().str.title()
        df["subcategory"] = df["subcategory"].astype(str).str.strip().str.title()
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0.0)
        df["unit_cost"] = pd.to_numeric(df["unit_cost"], errors="coerce").fillna(0.0)
        return df

    def transform_sales(self, df_orders: pd.DataFrame, df_order_items: pd.DataFrame, df_products: pd.DataFrame) -> pd.DataFrame:
        """
        Merges orders, order items, and products to compute fact_sales table.
        Computes revenue, cost, profit, and date_id integer format YYYYMMDD.
        """
        if df_orders.empty or df_order_items.empty:
            return pd.DataFrame()

        # Merge order items with orders
        df_merged = pd.merge(df_order_items, df_orders, on="order_id", how="inner")

        # Merge with product costs if unit_cost not present
        if "unit_cost" not in df_merged.columns and not df_products.empty:
            df_merged = pd.merge(
                df_merged, 
                df_products[["product_id", "unit_cost"]], 
                on="product_id", 
                how="left"
            )

        df = df_merged.copy()

        # Coerce numeric fields
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1).astype(int)
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0.0)
        df["unit_cost"] = pd.to_numeric(df["unit_cost"], errors="coerce").fillna(0.0)
        df["discount"] = pd.to_numeric(df["discount"], errors="coerce").fillna(0.0)

        # Ensure discount bounds [0, 1]
        df["discount"] = np.clip(df["discount"], 0.0, 1.0)

        # Calculated financial metrics
        df["revenue"] = np.round(df["quantity"] * df["unit_price"] * (1.0 - df["discount"]), 2)
        df["cost"] = np.round(df["quantity"] * df["unit_cost"], 2)
        df["profit"] = np.round(df["revenue"] - df["cost"], 2)

        # Date ID integer formatting
        if "date_id" not in df.columns or df["date_id"].isnull().any():
            if "order_date" in df.columns:
                df["date_id"] = pd.to_datetime(df["order_date"], errors="coerce").dt.strftime("%Y%m%d").astype(float).fillna(20240101).astype(int)
            else:
                df["date_id"] = 20240101

        # Clean column selection for fact_sales
        cols = ["order_id", "date_id", "customer_id", "product_id", "region_id", "employee_id", "quantity", "unit_price", "unit_cost", "discount", "revenue", "cost", "profit"]
        existing_cols = [c for c in cols if c in df.columns]
        return df[existing_cols]

def transform_data(extracted_datasets: dict) -> dict:
    transformer = DataTransformer()
    transformed = {}

    transformed["dim_region"] = transformer.transform_regions(extracted_datasets.get("regions", pd.DataFrame()))
    transformed["dim_customer"] = transformer.transform_customers(extracted_datasets.get("customers", pd.DataFrame()))
    transformed["dim_product"] = transformer.transform_products(extracted_datasets.get("products", pd.DataFrame()))
    transformed["dim_date"] = extracted_datasets.get("dim_date", pd.DataFrame())

    df_orders = extracted_datasets.get("orders", pd.DataFrame())
    df_order_items = extracted_datasets.get("order_items", pd.DataFrame())
    df_products = transformed["dim_product"]

    transformed["fact_sales"] = transformer.transform_sales(df_orders, df_order_items, df_products)
    logger.info("Data Transformation completed successfully.")
    return transformed
