"""
InsightBI AI — Fast Data Seeder (scripts/seed_processed_data.py)
Generates rich, fully populated analytical CSV datasets directly in data/processed/.
"""

import os
import pandas as pd
import numpy as np

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

def seed():
    print("🌱 Seeding analytical datasets into data/processed/...")

    # 1. Products Clean
    products = [
        {"product_id": 101, "sku": "SKU-TEC-LAP-0101", "product_name": "Enterprise Laptop Pro 15", "category": "Technology", "subcategory": "Laptops", "unit_cost": 800.0, "unit_price": 1200.0},
        {"product_id": 102, "sku": "SKU-TEC-MON-0102", "product_name": "UltraWide Monitor 34-Inch", "category": "Technology", "subcategory": "Monitors", "unit_cost": 360.0, "unit_price": 600.0},
        {"product_id": 103, "sku": "SKU-FUR-CHA-0103", "product_name": "Ergonomic Office Chair", "category": "Furniture", "subcategory": "Office Chairs", "unit_cost": 200.0, "unit_price": 350.0},
        {"product_id": 104, "sku": "SKU-FUR-DES-0104", "product_name": "Standing Desk Electric", "category": "Furniture", "subcategory": "Desks & Tables", "unit_cost": 400.0, "unit_price": 700.0},
        {"product_id": 105, "sku": "SKU-SOF-CLA-0105", "product_name": "Cloud License Enterprise", "category": "Software", "subcategory": "SaaS Subscriptions", "unit_cost": 40.0, "unit_price": 200.0},
        {"product_id": 106, "sku": "SKU-TEC-SMA-0106", "product_name": "Smartphone Pro Max", "category": "Technology", "subcategory": "Smartphones", "unit_cost": 600.0, "unit_price": 999.0},
        {"product_id": 107, "sku": "SKU-OFF-STO-0107", "product_name": "Storage Filing Cabinet", "category": "Office Supplies", "subcategory": "Storage & Organization", "unit_cost": 50.0, "unit_price": 120.0},
        {"product_id": 108, "sku": "SKU-CON-AUD-0108", "product_name": "Noise Cancelling Headphones", "category": "Consumer Electronics", "subcategory": "Audio & Headphones", "unit_cost": 120.0, "unit_price": 250.0}
    ]
    df_products = pd.DataFrame(products)
    df_products.to_csv(os.path.join(PROCESSED_DIR, "products_clean.csv"), index=False)

    # 2. Customers Clean
    customers = [
        {"customer_id": 1, "customer_code": "CUST-000001", "first_name": "James", "last_name": "Smith", "email": "james.smith@example.com", "registration_date": "2023-01-15", "customer_segment": "Enterprise", "credit_limit": 10000.0},
        {"customer_id": 2, "customer_code": "CUST-000002", "first_name": "Jennifer", "last_name": "Johnson", "email": "jennifer.johnson@example.com", "registration_date": "2023-02-20", "customer_segment": "Corporate", "credit_limit": 5000.0},
        {"customer_id": 3, "customer_code": "CUST-000003", "first_name": "Robert", "last_name": "Williams", "email": "robert.williams@example.com", "registration_date": "2023-03-10", "customer_segment": "SMB", "credit_limit": 2500.0},
        {"customer_id": 4, "customer_code": "CUST-000004", "first_name": "Sarah", "last_name": "Brown", "email": "sarah.brown@example.com", "registration_date": "2023-04-05", "customer_segment": "Consumer", "credit_limit": 1000.0},
        {"customer_id": 5, "customer_code": "CUST-000005", "first_name": "Michael", "last_name": "Jones", "email": "michael.jones@example.com", "registration_date": "2023-05-12", "customer_segment": "SMB", "credit_limit": 2500.0},
        {"customer_id": 6, "customer_code": "CUST-000006", "first_name": "Patricia", "last_name": "Miller", "email": "patricia.miller@example.com", "registration_date": "2023-06-18", "customer_segment": "Enterprise", "credit_limit": 10000.0},
        {"customer_id": 7, "customer_code": "CUST-000007", "first_name": "Linda", "last_name": "Davis", "email": "linda.davis@example.com", "registration_date": "2023-07-22", "customer_segment": "Corporate", "credit_limit": 5000.0},
        {"customer_id": 8, "customer_code": "CUST-000008", "first_name": "Elizabeth", "last_name": "Garcia", "email": "elizabeth.garcia@example.com", "registration_date": "2023-08-30", "customer_segment": "Consumer", "credit_limit": 1000.0}
    ]
    df_customers = pd.DataFrame(customers)
    df_customers.to_csv(os.path.join(PROCESSED_DIR, "customers_clean.csv"), index=False)

    # 3. Fact Sales Clean (Monthly Sales spanning 2024)
    sales = []
    sid = 1
    months = [
        ("2024-01-15", 20240115, "2024-01"),
        ("2024-02-18", 20240218, "2024-02"),
        ("2024-03-20", 20240320, "2024-03"),
        ("2024-04-12", 20240412, "2024-04"),
        ("2024-05-25", 20240525, "2024-05"),
        ("2024-06-30", 20240630, "2024-06")
    ]

    for date_str, date_id, ym in months:
        for p in products:
            for c in customers[:4]:
                qty = np.random.randint(2, 10)
                disc = 0.05
                rev = round(qty * p["unit_price"] * (1 - disc), 2)
                cst = round(qty * p["unit_cost"], 2)
                prf = round(rev - cst, 2)
                sales.append({
                    "sales_id": sid,
                    "order_id": f"ORD-{sid:06d}",
                    "date": date_str,
                    "date_id": date_id,
                    "customer_id": c["customer_id"],
                    "product_id": p["product_id"],
                    "region_id": (c["customer_id"] % 4) + 1,
                    "quantity": qty,
                    "unit_price": p["unit_price"],
                    "unit_cost": p["unit_cost"],
                    "discount": disc,
                    "revenue": rev,
                    "cost": cst,
                    "profit": prf
                })
                sid += 1

    df_sales = pd.DataFrame(sales)
    df_sales.to_csv(os.path.join(PROCESSED_DIR, "sales_clean.csv"), index=False)

    # 4. Customer Segments
    segments = [
        {"customer_id": 1, "customer_code": "CUST-000001", "first_name": "James", "last_name": "Smith", "email": "james.smith@example.com", "recency_days": 12, "frequency_count": 28, "monetary_value": 14500.50, "r_score": 5, "f_score": 5, "m_score": 5, "rfm_score": 555, "rfm_segment": "VIP / Champions"},
        {"customer_id": 2, "customer_code": "CUST-000002", "first_name": "Jennifer", "last_name": "Johnson", "email": "jennifer.johnson@example.com", "recency_days": 18, "frequency_count": 19, "monetary_value": 9820.00, "r_score": 5, "f_score": 4, "m_score": 4, "rfm_score": 544, "rfm_segment": "VIP / Champions"},
        {"customer_id": 3, "customer_code": "CUST-000003", "first_name": "Robert", "last_name": "Williams", "email": "robert.williams@example.com", "recency_days": 35, "frequency_count": 14, "monetary_value": 6450.25, "r_score": 4, "f_score": 4, "m_score": 4, "rfm_score": 444, "rfm_segment": "Loyal Customers"},
        {"customer_id": 4, "customer_code": "CUST-000004", "first_name": "Sarah", "last_name": "Brown", "email": "sarah.brown@example.com", "recency_days": 42, "frequency_count": 11, "monetary_value": 4890.00, "r_score": 3, "f_score": 3, "m_score": 3, "rfm_score": 333, "rfm_segment": "Potential Loyalists"},
        {"customer_id": 5, "customer_code": "CUST-000005", "first_name": "Michael", "last_name": "Jones", "email": "michael.jones@example.com", "recency_days": 95, "frequency_count": 3, "monetary_value": 850.00, "r_score": 1, "f_score": 1, "m_score": 1, "rfm_score": 111, "rfm_segment": "At-Risk / Lost"}
    ]
    pd.DataFrame(segments).to_csv(os.path.join(PROCESSED_DIR, "customer_segments.csv"), index=False)

    # 5. Forecast Predictions
    forecasts = [
        {"ds": "2024-07-01", "yhat": 265000.0, "yhat_lower": 245000.0, "yhat_upper": 285000.0, "territory": "Overall"},
        {"ds": "2024-08-01", "yhat": 278000.0, "yhat_lower": 258000.0, "yhat_upper": 298000.0, "territory": "Overall"},
        {"ds": "2024-09-01", "yhat": 295000.0, "yhat_lower": 272000.0, "yhat_upper": 318000.0, "territory": "Overall"},
        {"ds": "2024-10-01", "yhat": 310000.0, "yhat_lower": 285000.0, "yhat_upper": 335000.0, "territory": "Overall"},
        {"ds": "2024-11-01", "yhat": 385000.0, "yhat_lower": 350000.0, "yhat_upper": 420000.0, "territory": "Overall"},
        {"ds": "2024-12-01", "yhat": 425000.0, "yhat_lower": 390000.0, "yhat_upper": 460000.0, "territory": "Overall"}
    ]
    pd.DataFrame(forecasts).to_csv(os.path.join(PROCESSED_DIR, "forecast_predictions.csv"), index=False)

    # 6. Sales Anomalies
    anomalies = [
        {"sales_id": 1402, "order_id": "ORD-0001402", "date": "2024-04-12", "revenue": 45000.0, "anomaly_score": -0.42, "reason": "Unusual bulk order volume spiking 450% above baseline"},
        {"sales_id": 2891, "order_id": "ORD-0002891", "date": "2024-05-28", "revenue": 62000.0, "anomaly_score": -0.58, "reason": "High single-transaction value for Enterprise Cloud License"}
    ]
    pd.DataFrame(anomalies).to_csv(os.path.join(PROCESSED_DIR, "sales_anomalies.csv"), index=False)

    print(f"✅ Seeding Complete! Generated {len(sales)} sales records across 8 products & 8 customers.")

if __name__ == "__main__":
    seed()
