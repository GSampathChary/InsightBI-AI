"""
InsightBI AI — ETL Module: Extract (etl/extract.py)
Extracts raw business datasets from data/raw/ directory.
"""

import os
import logging
import pandas as pd
from typing import Dict

logger = logging.getLogger("insightbi.etl.extract")

class DataExtractor:
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
        else:
            self.data_dir = data_dir

    def extract_raw_datasets(()) -> Dict[str, pd.DataFrame]:
        """Reads raw CSV files and returns dictionary of DataFrames."""
        datasets = {}
        files = {
            "regions": "regions.csv",
            "customers": "customers.csv",
            "products": "products.csv",
            "campaigns": "campaigns.csv",
            "dim_date": "dim_date.csv",
            "orders": "orders.csv",
            "order_items": "order_items.csv"
        }

        for key, filename in files.items():
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                df = pd.read_csv(filepath)
                datasets[key] = df
                logger.info(f"Extracted {len(df):,} rows from {filename}")
            else:
                logger.warning(f"File not found: {filepath}. Returning empty DataFrame for '{key}'.")
                datasets[key] = pd.DataFrame()

        return datasets

def extract_data(data_dir: str = None) -> Dict[str, pd.DataFrame]:
    extractor = DataExtractor(data_dir=data_dir)
    return extractor.extract_raw_datasets()
