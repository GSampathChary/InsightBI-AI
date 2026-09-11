"""
InsightBI AI — ETL Module: Validate (etl/validate.py)
Performs data quality checks: duplicate removal, null checks, negative value detection,
foreign key orphan checks, and quality score reporting.
"""

import logging
import pandas as pd
from typing import Dict, Tuple, Any

logger = logging.getLogger("insightbi.etl.validate")

class DataValidator:
    def __init__(self):
        self.report = {
            "total_rows_processed": 0,
            "valid_rows": 0,
            "invalid_rows": 0,
            "duplicates_removed": 0,
            "nulls_detected": 0,
            "quality_score_percent": 100.0,
            "details": {}
        }

    def validate_dataset(self, transformed_datasets: Dict[str, pd.DataFrame]) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
        """Validates transformed datasets and filters out invalid records."""
        cleaned_datasets = {}
        total_rows = 0
        total_valid = 0
        total_invalid = 0
        total_duplicates = 0
        total_nulls = 0

        # Validate Customers
        if "dim_customer" in transformed_datasets and not transformed_datasets["dim_customer"].empty:
            df = transformed_datasets["dim_customer"]
            t_count = len(df)
            total_rows += t_count
            
            # Duplicates check
            df_clean = df.drop_duplicates(subset=["customer_id"])
            dups = t_count - len(df_clean)
            total_duplicates += dups
            
            # Nulls check
            null_mask = df_clean["customer_id"].isnull() | df_clean["email"].isnull()
            null_count = null_mask.sum()
            total_nulls += null_count
            
            df_valid = df_clean[~null_mask]
            total_valid += len(df_valid)
            total_invalid += (t_count - len(df_valid))
            cleaned_datasets["dim_customer"] = df_valid
            self.report["details"]["dim_customer"] = {"total": t_count, "valid": len(df_valid), "duplicates": dups, "nulls": null_count}

        # Validate Products
        if "dim_product" in transformed_datasets and not transformed_datasets["dim_product"].empty:
            df = transformed_datasets["dim_product"]
            t_count = len(df)
            total_rows += t_count
            
            df_clean = df.drop_duplicates(subset=["product_id"])
            dups = t_count - len(df_clean)
            total_duplicates += dups
            
            # Check negative cost/price
            neg_mask = (df_clean["unit_price"] < 0) | (df_clean["unit_cost"] < 0)
            null_mask = df_clean["product_id"].isnull() | df_clean["sku"].isnull()
            invalid_mask = neg_mask | null_mask
            
            df_valid = df_clean[~invalid_mask]
            total_valid += len(df_valid)
            total_invalid += (t_count - len(df_valid))
            cleaned_datasets["dim_product"] = df_valid
            self.report["details"]["dim_product"] = {"total": t_count, "valid": len(df_valid), "duplicates": dups, "invalid_values": int(neg_mask.sum())}

        # Validate Fact Sales
        if "fact_sales" in transformed_datasets and not transformed_datasets["fact_sales"].empty:
            df = transformed_datasets["fact_sales"]
            t_count = len(df)
            total_rows += t_count

            # Duplicates check
            df_clean = df.drop_duplicates(subset=["order_id", "product_id"])
            dups = t_count - len(df_clean)
            total_duplicates += dups

            # Validation rules:
            # 1. quantity > 0
            # 2. revenue >= 0
            # 3. customer_id, product_id, date_id not null
            invalid_mask = (
                (df_clean["quantity"] <= 0) |
                (df_clean["revenue"] < 0) |
                (df_clean["customer_id"].isnull()) |
                (df_clean["product_id"].isnull()) |
                (df_clean["date_id"].isnull())
            )

            # Foreign key orphan check if dimension datasets present
            if "dim_customer" in cleaned_datasets:
                valid_cust_ids = set(cleaned_datasets["dim_customer"]["customer_id"].values)
                orphan_cust_mask = ~df_clean["customer_id"].isin(valid_cust_ids)
                invalid_mask = invalid_mask | orphan_cust_mask

            if "dim_product" in cleaned_datasets:
                valid_prod_ids = set(cleaned_datasets["dim_product"]["product_id"].values)
                orphan_prod_mask = ~df_clean["product_id"].isin(valid_prod_ids)
                invalid_mask = invalid_mask | orphan_prod_mask

            df_valid = df_clean[~invalid_mask]
            invalid_cnt = t_count - len(df_valid)
            
            total_valid += len(df_valid)
            total_invalid += invalid_cnt
            cleaned_datasets["fact_sales"] = df_valid
            self.report["details"]["fact_sales"] = {"total": t_count, "valid": len(df_valid), "duplicates": dups, "rejected": invalid_cnt}

        # Pass through remaining dimension tables
        for k in ["dim_region", "dim_date", "dim_campaign"]:
            if k in transformed_datasets:
                cleaned_datasets[k] = transformed_datasets[k]

        # Calculate final quality score
        self.report["total_rows_processed"] = total_rows
        self.report["valid_rows"] = total_valid
        self.report["invalid_rows"] = total_invalid
        self.report["duplicates_removed"] = total_duplicates
        self.report["nulls_detected"] = total_nulls
        if total_rows > 0:
            self.report["quality_score_percent"] = round((total_valid / total_rows) * 100.0, 2)
        else:
            self.report["quality_score_percent"] = 100.0

        logger.info(f"Data Validation completed. Quality Score: {self.report['quality_score_percent']}%")
        return cleaned_datasets, self.report

def validate_data(transformed_datasets: dict) -> Tuple[dict, dict]:
    validator = DataValidator()
    return validator.validate_dataset(transformed_datasets)
