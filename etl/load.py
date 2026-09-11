"""
InsightBI AI — ETL Module: Load (etl/load.py)
Loads cleaned datasets into PostgreSQL database tables or outputs clean CSV files to data/processed/.
"""

import os
import logging
import pandas as pd
from sqlalchemy import create_engine
from app.core.config import settings

logger = logging.getLogger("insightbi.etl.load")

class DataLoader:
    def __init__(self, db_url: str = None):
        self.db_url = db_url or settings.DATABASE_URL
        self.output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
        os.makedirs(self.output_dir, exist_ok=True)

    def load_to_csv(self, validated_datasets: dict):
        """Saves clean dataframes to data/processed/ CSV files."""
        name_map = {
            "dim_customer": "customers_clean.csv",
            "dim_product": "products_clean.csv",
            "fact_sales": "sales_clean.csv",
            "dim_region": "regions_clean.csv"
        }

        for key, df in validated_datasets.items():
            if not df.empty and key in name_map:
                filepath = os.path.join(self.output_dir, name_map[key])
                df.to_csv(filepath, index=False)
                logger.info(f"Saved {len(df):,} clean rows to {filepath}")

    def load_to_postgres(self, validated_datasets: dict):
        """Batch loads clean dataframes into PostgreSQL database tables."""
        try:
            engine = create_engine(self.db_url)
            files_to_tables = [
                ("dim_region", "dim_region"),
                ("dim_date", "dim_date"),
                ("dim_product", "dim_product"),
                ("dim_customer", "dim_customer"),
                ("fact_sales", "fact_sales")
            ]

            with engine.begin() as conn:
                for dataset_key, table_name in files_to_tables:
                    if dataset_key in validated_datasets and not validated_datasets[dataset_key].empty:
                        df = validated_datasets[dataset_key]
                        df.to_sql(table_name, con=conn, if_exists="append", index=False, method="multi", chunksize=5000)
                        logger.info(f"Loaded {len(df):,} rows into PostgreSQL table '{table_name}'")
            return True
        except Exception as e:
            logger.warning(f"PostgreSQL load skipped/deferred ({e}). Data persisted to CSV.")
            return False

def load_data(validated_datasets: dict) -> bool:
    loader = DataLoader()
    loader.load_to_csv(validated_datasets)
    db_success = loader.load_to_postgres(validated_datasets)
    return db_success
