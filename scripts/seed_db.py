"""
InsightBI AI — Database Seeder
Loads synthetic CSV files from data/raw/ and data/processed/ into PostgreSQL database tables.
Supports SQLAlchemy ORM & psycopg2 / SQLite fallback for verification.
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from app.core.config import settings

def load_data_to_db():
    print(f"Connecting to database: {settings.DB_NAME} at {settings.DB_HOST}...")
    engine = create_engine(settings.DATABASE_URL)
    
    data_raw = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    data_proc = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

    # Order of insertion to respect foreign keys
    files_to_tables = [
        (os.path.join(data_raw, "regions.csv"), "dim_region"),
        (os.path.join(data_raw, "dim_date.csv"), "dim_date"),
        (os.path.join(data_raw, "products.csv"), "dim_product"),
        (os.path.join(data_raw, "customers.csv"), "dim_customer"),
        (os.path.join(data_raw, "campaigns.csv"), "dim_campaign"),
        (os.path.join(data_proc, "sales_clean.csv"), "fact_sales"),
    ]

    with engine.begin() as conn:
        for file_path, table_name in files_to_tables:
            if not os.path.exists(file_path):
                print(f"⚠️ File not found: {file_path}. Run python scripts/generate_data.py first.")
                continue

            print(f"Loading {file_path} into table '{table_name}'...")
            df = pd.read_csv(file_path)
            
            # Append data to SQL database
            df.to_sql(table_name, con=conn, if_exists="append", index=False, method="multi", chunksize=5000)
            print(f"✓ Loaded {len(df):,} rows into {table_name}")

    print("\n✅ Database Seeding Successfully Completed!")

if __name__ == "__main__":
    load_data_to_db()
