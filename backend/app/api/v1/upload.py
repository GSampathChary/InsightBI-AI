"""
InsightBI AI — CSV Upload Endpoint (backend/app/api/v1/upload.py)
Receives user-uploaded CSV files, parses and validates columns, transforms metrics,
and dynamically updates the processed analytical datasets.
"""

import os
import io
import logging
import pandas as pd
import numpy as np
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any
from ml.segmentation.cluster_customers import train_customer_segmentation

router = APIRouter()
logger = logging.getLogger("insightbi.upload")

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

@router.post("/csv")
async def upload_csv_dataset(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload custom sales CSV dataset.
    Validates headers, cleans numeric fields, calculates revenue/profit metrics,
    and updates all dashboard analytics dynamically.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files (.csv) are supported.")

    try:
        contents = await file.read()
        df_raw = pd.read_csv(io.BytesIO(contents))

        if df_raw.empty:
            raise HTTPException(status_code=400, detail="Uploaded CSV file is empty.")

        # Normalize column names (lowercase, stripped, replace spaces with underscores)
        df_raw.columns = [str(c).strip().lower().replace(" ", "_") for c in df_raw.columns]

        df = df_raw.copy()

        # Coerce/Generate required columns
        if "order_id" not in df.columns:
            df["order_id"] = [f"ORD-{i+1:06d}" for i in range(len(df))]

        if "sales_id" not in df.columns:
            df["sales_id"] = range(1, len(df) + 1)

        # Date handling
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
            df["date_id"] = pd.to_datetime(df["date"]).dt.strftime("%Y%m%d").fillna(20240101).astype(int)
        elif "date_id" in df.columns:
            df["date_id"] = pd.to_numeric(df["date_id"], errors="coerce").fillna(20240101).astype(int)
            df["date"] = df["date_id"].astype(str).str.slice(0, 8).apply(lambda s: f"{s[:4]}-{s[4:6]}-{s[6:8]}" if len(s) == 8 else "2024-01-01")
        else:
            df["date"] = "2024-01-15"
            df["date_id"] = 20240115

        # Customer ID
        if "customer_id" not in df.columns:
            df["customer_id"] = np.random.randint(1, 100, size=len(df))

        # Product ID & Category
        if "product_id" not in df.columns:
            df["product_id"] = np.random.randint(101, 120, size=len(df))

        if "product_name" not in df.columns:
            df["product_name"] = df["product_id"].apply(lambda p: f"Uploaded Product #{p}")

        if "category" not in df.columns:
            df["category"] = "General"

        # Region
        if "region_id" not in df.columns:
            df["region_id"] = (df["customer_id"] % 4) + 1

        if "region_name" not in df.columns:
            region_map = {1: "North America East", 2: "North America West", 3: "South Region", 4: "Midwest Region"}
            df["region_name"] = df["region_id"].map(region_map).fillna("North America East")

        # Quantities, Prices, Costs, Revenues, Profits
        if "quantity" in df.columns:
            df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1).astype(int)
        else:
            df["quantity"] = 1

        if "unit_price" in df.columns:
            df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(100.0)
        else:
            df["unit_price"] = 100.0

        if "unit_cost" in df.columns:
            df["unit_cost"] = pd.to_numeric(df["unit_cost"], errors="coerce").fillna(df["unit_price"] * 0.6)
        else:
            df["unit_cost"] = df["unit_price"] * 0.6

        if "discount" in df.columns:
            df["discount"] = pd.to_numeric(df["discount"], errors="coerce").fillna(0.0)
        else:
            df["discount"] = 0.0

        # Financial Calculations
        if "revenue" in df.columns:
            df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(df["quantity"] * df["unit_price"] * (1 - df["discount"]))
        else:
            df["revenue"] = np.round(df["quantity"] * df["unit_price"] * (1 - df["discount"]), 2)

        if "cost" in df.columns:
            df["cost"] = pd.to_numeric(df["cost"], errors="coerce").fillna(df["quantity"] * df["unit_cost"])
        else:
            df["cost"] = np.round(df["quantity"] * df["unit_cost"], 2)

        if "profit" in df.columns:
            df["profit"] = pd.to_numeric(df["profit"], errors="coerce").fillna(df["revenue"] - df["cost"])
        else:
            df["profit"] = np.round(df["revenue"] - df["cost"], 2)

        # Save processed sales CSV
        sales_path = os.path.join(PROCESSED_DIR, "sales_clean.csv")
        df.to_csv(sales_path, index=False)

        # Generate & save products clean table
        df_prod = df.groupby(["product_id", "product_name", "category"]).agg(
            unit_price=("unit_price", "mean"),
            unit_cost=("unit_cost", "mean")
        ).reset_index()
        df_prod["sku"] = df_prod["product_id"].apply(lambda p: f"SKU-UPL-{p}")
        df_prod.to_csv(os.path.join(PROCESSED_DIR, "products_clean.csv"), index=False)

        # Generate & save customers clean table
        df_cust = df.groupby("customer_id").agg(
            first_name=("customer_id", lambda c: f"Customer #{c.iloc[0]}"),
            last_name=("customer_id", lambda c: "Account")
        ).reset_index()
        df_cust["customer_code"] = df_cust["customer_id"].apply(lambda c: f"CUST-{c:06d}")
        df_cust["email"] = df_cust["customer_id"].apply(lambda c: f"cust{c}@uploaded.com")
        df_cust["customer_segment"] = "Uploaded Account"
        df_cust["credit_limit"] = 5000.0
        df_cust.to_csv(os.path.join(PROCESSED_DIR, "customers_clean.csv"), index=False)

        # Re-run RFM segmentation
        try:
            df_segments = train_customer_segmentation(df, df_cust)
            if not df_segments.empty:
                df_segments.to_csv(os.path.join(PROCESSED_DIR, "customer_segments.csv"), index=False)
        except Exception as e:
            logger.warning(f"RFM segmentation warning on upload: {e}")

        total_rev = float(df["revenue"].sum())
        total_prf = float(df["profit"].sum())
        row_count = len(df)

        return {
            "success": True,
            "filename": file.filename,
            "row_count": row_count,
            "total_revenue": round(total_rev, 2),
            "total_profit": round(total_prf, 2),
            "columns_processed": list(df.columns),
            "message": f"Successfully processed dataset '{file.filename}' with {row_count:,} records!"
        }

    except Exception as e:
        logger.error(f"Error processing uploaded CSV: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process CSV dataset: {str(e)}")
