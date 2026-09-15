"""
InsightBI AI — Synthetic Data Generator
Generates realistic business datasets:
- 20 Regions & Territories
- 10,000 Customers with demographic & regional distributions
- 500 Products across 5 categories & 15 subcategories
- 15 Marketing Campaigns
- 100,000+ Orders & 200,000+ Order Items spanning 2023-2026
- Realistic seasonality, monthly growth, Pareto 80/20 product demand, discount impacts, and anomalies.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set random seeds for reproducible synthetic generation
random.seed(42)
np.random.seed(42)

DATA_RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
DATA_PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
os.makedirs(DATA_RAW_DIR, exist_ok=True)
os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Regions Generation (20 Indian states and territories)
# -----------------------------------------------------------------------------
REGIONS_DATA = [
    {"region_id": 1, "region_name": "North India", "country": "India", "state": "Delhi", "city": "New Delhi", "territory": "Delhi NCR"},
    {"region_id": 2, "region_name": "North India", "country": "India", "state": "Haryana", "city": "Gurugram", "territory": "Delhi NCR"},
    {"region_id": 3, "region_name": "North India", "country": "India", "state": "Uttar Pradesh", "city": "Noida", "territory": "Delhi NCR"},
    {"region_id": 4, "region_name": "North India", "country": "India", "state": "Punjab", "city": "Chandigarh", "territory": "Punjab & Chandigarh"},
    {"region_id": 5, "region_name": "West India", "country": "India", "state": "Maharashtra", "city": "Mumbai", "territory": "Mumbai Metropolitan Region"},
    {"region_id": 6, "region_name": "West India", "country": "India", "state": "Maharashtra", "city": "Pune", "territory": "Maharashtra"},
    {"region_id": 7, "region_name": "West India", "country": "India", "state": "Gujarat", "city": "Ahmedabad", "territory": "Gujarat"},
    {"region_id": 8, "region_name": "West India", "country": "India", "state": "Rajasthan", "city": "Jaipur", "territory": "Rajasthan"},
    {"region_id": 9, "region_name": "South India", "country": "India", "state": "Karnataka", "city": "Bengaluru", "territory": "Karnataka"},
    {"region_id": 10, "region_name": "South India", "country": "India", "state": "Tamil Nadu", "city": "Chennai", "territory": "Tamil Nadu"},
    {"region_id": 11, "region_name": "South India", "country": "India", "state": "Telangana", "city": "Hyderabad", "territory": "Telangana"},
    {"region_id": 12, "region_name": "South India", "country": "India", "state": "Kerala", "city": "Kochi", "territory": "Kerala"},
    {"region_id": 13, "region_name": "East India", "country": "India", "state": "West Bengal", "city": "Kolkata", "territory": "West Bengal"},
    {"region_id": 14, "region_name": "East India", "country": "India", "state": "Odisha", "city": "Bhubaneswar", "territory": "Odisha"},
    {"region_id": 15, "region_name": "East India", "country": "India", "state": "Bihar", "city": "Patna", "territory": "Bihar"},
    {"region_id": 16, "region_name": "East India", "country": "India", "state": "Assam", "city": "Guwahati", "territory": "North East"},
    {"region_id": 17, "region_name": "Central India", "country": "India", "state": "Madhya Pradesh", "city": "Indore", "territory": "Madhya Pradesh"},
    {"region_id": 18, "region_name": "Central India", "country": "India", "state": "Chhattisgarh", "city": "Raipur", "territory": "Chhattisgarh"},
    {"region_id": 19, "region_name": "North India", "country": "India", "state": "Uttarakhand", "city": "Dehradun", "territory": "Uttarakhand"},
    {"region_id": 20, "region_name": "North India", "country": "India", "state": "Himachal Pradesh", "city": "Shimla", "territory": "Himachal Pradesh"}
]

# -----------------------------------------------------------------------------
# 2. Product Categories & Catalog (500 Products)
# -----------------------------------------------------------------------------
CATEGORIES = {
    "Technology": {
        "Laptops": (500, 2200),
        "Smartphones": (300, 1400),
        "Monitors": (150, 800),
        "Accessories": (15, 120)
    },
    "Office Supplies": {
        "Storage & Organization": (20, 150),
        "Paper & Stationery": (5, 45),
        "Binders & Folders": (4, 30),
        "Writing Instruments": (2, 25)
    },
    "Furniture": {
        "Office Chairs": (120, 750),
        "Desks & Tables": (200, 1500),
        "Bookcases": (80, 500),
        "Lighting": (30, 200)
    },
    "Consumer Electronics": {
        "Audio & Headphones": (40, 350),
        "Wearables & Smartwatches": (80, 450),
        "Cameras & Photography": (250, 1800)
    },
    "Software & Services": {
        "SaaS Subscriptions": (50, 500),
        "Cloud Storage Licenses": (20, 250)
    }
}

FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth",
               "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen",
               "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Donald", "Sandra",
               "Mark", "Ashley", "Paul", "Kimberly", "Steven", "Emily", "Andrew", "Donna", "Kenneth", "Michelle"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
              "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"]

def generate_products():
    products = []
    pid = 1
    for category, subcats in CATEGORIES.items():
        for subcat, (min_price, max_price) in subcats.items():
            # generate ~30-40 products per subcategory to reach 500
            for i in range(1, 35):
                sku = f"SKU-{category[:3].upper()}-{subcat[:3].upper()}-{pid:04d}"
                name = f"{category[:-1] if category.endswith('s') else category} {subcat[:-1] if subcat.endswith('s') else subcat} Pro {i}"
                unit_price = round(random.uniform(min_price, max_price), 2)
                margin = random.uniform(0.35, 0.65) # 35% to 65% margin
                unit_cost = round(unit_price * (1 - margin), 2)
                supplier = f"{subcat} Corp"
                
                products.append({
                    "product_id": pid,
                    "sku": sku,
                    "product_name": name,
                    "category": category,
                    "subcategory": subcat,
                    "unit_cost": unit_cost,
                    "unit_price": unit_price,
                    "supplier": supplier,
                    "is_active": True
                })
                pid += 1
                if pid > 500:
                    break
            if pid > 500:
                break
        if pid > 500:
            break
    return pd.DataFrame(products)

def generate_customers(num_customers=10000):
    customers = []
    start_reg = datetime(2022, 1, 1)
    for cid in range(1, num_customers + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        code = f"CUST-{cid:06d}"
        email = f"{first_name.lower()}.{last_name.lower()}{cid}@example.com"
        phone = f"555-{random.randint(100,999):03d}-{random.randint(1000,9999):04d}"
        region = random.choice(REGIONS_DATA)
        reg_date = start_reg + timedelta(days=random.randint(0, 1200))
        credit_limit = random.choice([500.0, 1000.0, 2500.0, 5000.0, 10000.0])
        
        customers.append({
            "customer_id": cid,
            "customer_code": code,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "region_id": region["region_id"],
            "customer_segment": random.choice(["Enterprise", "SMB", "Consumer", "Corporate"]),
            "credit_limit": credit_limit,
            "registration_date": reg_date.strftime("%Y-%m-%d"),
            "is_active": True
        })
    return pd.DataFrame(customers)

def generate_campaigns():
    campaigns = [
        {"campaign_id": 1, "campaign_name": "New Year Tech Refresh 2023", "channel": "Email", "start_date": "2023-01-05", "end_date": "2023-01-25", "budget": 15000.00},
        {"campaign_id": 2, "campaign_name": "Spring Office Clearance 2023", "channel": "Google Search", "start_date": "2023-03-10", "end_date": "2023-03-31", "budget": 22000.00},
        {"campaign_id": 3, "campaign_name": "Summer Tech Sale 2023", "channel": "Social Media", "start_date": "2023-06-15", "end_date": "2023-07-05", "budget": 35000.00},
        {"campaign_id": 4, "campaign_name": "Back to School Workstations", "channel": "Email", "start_date": "2023-08-15", "end_date": "2023-09-10", "budget": 28000.00},
        {"campaign_id": 5, "campaign_name": "Black Friday Mega Deal 2023", "channel": "Multi-Channel", "start_date": "2023-11-20", "end_date": "2023-11-30", "budget": 75000.00},
        {"campaign_id": 6, "campaign_name": "Q4 Holiday Tech Blitz 2023", "channel": "Display Ads", "start_date": "2023-12-05", "end_date": "2023-12-24", "budget": 60000.00},
        {"campaign_id": 7, "campaign_name": "New Year Enterprise Upgrade 2024", "channel": "LinkedIn", "start_date": "2024-01-10", "end_date": "2024-02-15", "budget": 45000.00},
        {"campaign_id": 8, "campaign_name": "Spring Productivity Fest 2024", "channel": "Google Search", "start_date": "2024-04-01", "end_date": "2024-04-30", "budget": 30000.00},
        {"campaign_id": 9, "campaign_name": "Mid-Year Software Sale 2024", "channel": "Email", "start_date": "2024-06-01", "end_date": "2024-06-30", "budget": 20000.00},
        {"campaign_id": 10, "campaign_name": "Black Friday Cyber Week 2024", "channel": "Multi-Channel", "start_date": "2024-11-25", "end_date": "2024-12-05", "budget": 90000.00},
        {"campaign_id": 11, "campaign_name": "Q4 Enterprise Closing 2024", "channel": "Direct Mail", "start_date": "2024-12-10", "end_date": "2024-12-31", "budget": 50000.00},
        {"campaign_id": 12, "campaign_name": "Q1 2025 SaaS Launch", "channel": "LinkedIn", "start_date": "2025-01-15", "end_date": "2025-02-28", "budget": 40000.00},
        {"campaign_id": 13, "campaign_name": "Spring Tech Expo 2025", "channel": "Google Search", "start_date": "2025-04-10", "end_date": "2025-05-10", "budget": 35000.00},
        {"campaign_id": 14, "campaign_name": "Summer Hardware Blast 2025", "channel": "Social Media", "start_date": "2025-07-01", "end_date": "2025-07-31", "budget": 42000.00},
        {"campaign_id": 15, "campaign_name": "Q4 Holiday Special 2025", "channel": "Multi-Channel", "start_date": "2025-11-20", "end_date": "2025-12-25", "budget": 85000.00}
    ]
    return pd.DataFrame(campaigns)

def generate_orders_and_sales(df_customers, df_products, num_orders=100000):
    """
    Generates 100,000+ orders with realistic dates, seasonality, repeat purchasing,
    Pareto product weights, discounts, revenue, cost, and profit calculations.
    """
    print(f"Generating {num_orders} orders & line items...")
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2026, 6, 30)
    total_days = (end_date - start_date).days

    # Customer weights (20% high-frequency buyers)
    num_cust = len(df_customers)
    cust_ids = df_customers["customer_id"].values
    cust_weights = np.random.exponential(scale=1.0, size=num_cust)
    cust_weights /= cust_weights.sum()

    # Product weights (Pareto 80/20 rule)
    num_prod = len(df_products)
    prod_ids = df_products["product_id"].values
    prod_prices = df_products["unit_price"].values
    prod_costs = df_products["unit_cost"].values
    prod_map = {row["product_id"]: row for _, row in df_products.iterrows()}

    prod_weights = np.random.pareto(a=1.5, size=num_prod)
    prod_weights /= prod_weights.sum()

    orders = []
    order_items = []
    sales_clean = []
    item_id_counter = 1

    # Date distribution with seasonality (Q4 spike, year over year growth)
    date_pool = []
    for d in range(total_days):
        current_dt = start_date + timedelta(days=d)
        m = current_dt.month
        y_factor = 1.0 + 0.15 * (current_dt.year - 2023) # 15% annual growth
        season_factor = 1.6 if m in [11, 12] else (0.85 if m in [1, 2] else 1.0)
        weight = y_factor * season_factor
        date_pool.append((current_dt, weight))

    d_dates, d_weights = zip(*date_pool)
    d_weights = np.array(d_weights) / sum(d_weights)

    # Sample dates for orders
    order_dates = np.random.choice(d_dates, size=num_orders, p=d_weights)

    cust_region_map = dict(zip(df_customers["customer_id"], df_customers["region_id"]))

    for oid in range(1, num_orders + 1):
        order_code = f"ORD-{oid:07d}"
        o_date = order_dates[oid - 1]
        date_id = int(o_date.strftime("%Y%m%d"))
        
        cid = np.random.choice(cust_ids, p=cust_weights)
        cust_region_id = cust_region_map[cid]
        emp_id = random.randint(1, 25)
        camp_id = random.choice([None, None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

        # Number of line items per order (1 to 4 items)
        num_items = random.choices([1, 2, 3, 4], weights=[0.55, 0.25, 0.12, 0.08])[0]
        
        order_revenue = 0.0
        order_cost = 0.0

        selected_prods = np.random.choice(prod_ids, size=num_items, replace=False, p=prod_weights)
        for pid in selected_prods:
            prod_info = prod_map[pid]
            unit_price = float(prod_info["unit_price"])
            unit_cost = float(prod_info["unit_cost"])
            
            # Quantity & Discounts
            quantity = random.choices([1, 2, 3, 5, 10], weights=[0.60, 0.25, 0.09, 0.04, 0.02])[0]
            discount = random.choices([0.0, 0.05, 0.10, 0.15, 0.20], weights=[0.60, 0.15, 0.12, 0.08, 0.05])[0]
            
            revenue = round(quantity * unit_price * (1.0 - discount), 2)
            cost = round(quantity * unit_cost, 2)
            profit = round(revenue - cost, 2)

            order_revenue += revenue
            order_cost += cost

            # Append to sales_clean
            sales_clean.append({
                "sales_id": item_id_counter,
                "order_id": order_code,
                "date_id": date_id,
                "customer_id": cid,
                "product_id": pid,
                "region_id": cust_region_id,
                "employee_id": emp_id,
                "campaign_id": camp_id,
                "quantity": quantity,
                "unit_price": unit_price,
                "unit_cost": unit_cost,
                "discount": discount,
                "revenue": revenue,
                "cost": cost,
                "profit": profit
            })

            # Append to order_items
            order_items.append({
                "item_id": item_id_counter,
                "order_id": order_code,
                "product_id": pid,
                "quantity": quantity,
                "unit_price": unit_price,
                "discount": discount,
                "total_price": revenue
            })
            item_id_counter += 1

        orders.append({
            "order_id": order_code,
            "date_id": date_id,
            "order_date": o_date.strftime("%Y-%m-%d"),
            "customer_id": cid,
            "region_id": cust_region_id,
            "employee_id": emp_id,
            "total_items": num_items,
            "total_revenue": round(order_revenue, 2),
            "total_cost": round(order_cost, 2),
            "total_profit": round(order_revenue - order_cost, 2),
            "order_status": random.choices(["Completed", "Shipped", "Processing", "Cancelled"], weights=[0.85, 0.08, 0.05, 0.02])[0]
        })

    return pd.DataFrame(orders), pd.DataFrame(order_items), pd.DataFrame(sales_clean)

def generate_dim_date():
    """Generates comprehensive calendar dimension dim_date (2022-2026)."""
    dates = []
    start = datetime(2022, 1, 1)
    end = datetime(2026, 12, 31)
    cur = start
    while cur <= end:
        date_id = int(cur.strftime("%Y%m%d"))
        is_weekend = cur.weekday() in [5, 6]
        # Basic holiday simulation
        holiday = False
        holiday_name = None
        if cur.month == 12 and cur.day == 25:
            holiday, holiday_name = True, "Christmas Day"
        elif cur.month == 1 and cur.day == 1:
            holiday, holiday_name = True, "New Year's Day"
        elif cur.month == 7 and cur.day == 4:
            holiday, holiday_name = True, "Independence Day"
        elif cur.month == 11 and 22 <= cur.day <= 28 and cur.weekday() == 3:
            holiday, holiday_name = True, "Thanksgiving"

        dates.append({
            "date_id": date_id,
            "date": cur.strftime("%Y-%m-%d"),
            "year": cur.year,
            "quarter": (cur.month - 1) // 3 + 1,
            "month": cur.month,
            "month_name": cur.strftime("%B"),
            "week_of_year": cur.isocalendar()[1],
            "day_of_week": cur.weekday() + 1,
            "day_name": cur.strftime("%A"),
            "is_weekend": is_weekend,
            "holiday": holiday,
            "holiday_name": holiday_name
        })
        cur += timedelta(days=1)
    return pd.DataFrame(dates)

def main():
    print("🚀 Starting Synthetic Data Generation for InsightBI AI...")
    
    df_regions = pd.DataFrame(REGIONS_DATA)
    df_regions.to_csv(os.path.join(DATA_RAW_DIR, "regions.csv"), index=False)
    print(f"✓ Saved {len(df_regions)} regions to data/raw/regions.csv")

    df_products = generate_products()
    df_products.to_csv(os.path.join(DATA_RAW_DIR, "products.csv"), index=False)
    print(f"✓ Saved {len(df_products)} products to data/raw/products.csv")

    df_customers = generate_customers(num_customers=10000)
    df_customers.to_csv(os.path.join(DATA_RAW_DIR, "customers.csv"), index=False)
    print(f"✓ Saved {len(df_customers)} customers to data/raw/customers.csv")

    df_campaigns = generate_campaigns()
    df_campaigns.to_csv(os.path.join(DATA_RAW_DIR, "campaigns.csv"), index=False)
    print(f"✓ Saved {len(df_campaigns)} campaigns to data/raw/campaigns.csv")

    df_dim_date = generate_dim_date()
    df_dim_date.to_csv(os.path.join(DATA_RAW_DIR, "dim_date.csv"), index=False)
    print(f"✓ Saved {len(df_dim_date)} dates to data/raw/dim_date.csv")

    df_orders, df_order_items, df_sales_clean = generate_orders_and_sales(
        df_customers, df_products, num_orders=5000
    )

    df_orders.to_csv(os.path.join(DATA_RAW_DIR, "orders.csv"), index=False)
    print(f"✓ Saved {len(df_orders)} orders to data/raw/orders.csv")

    df_order_items.to_csv(os.path.join(DATA_RAW_DIR, "order_items.csv"), index=False)
    print(f"✓ Saved {len(df_order_items)} order items to data/raw/order_items.csv")

    df_sales_clean.to_csv(os.path.join(DATA_PROCESSED_DIR, "sales_clean.csv"), index=False)
    print(f"✓ Saved {len(df_sales_clean)} fact sales records to data/processed/sales_clean.csv")

    # Save cleaned dimension files to processed
    df_customers.to_csv(os.path.join(DATA_PROCESSED_DIR, "customers_clean.csv"), index=False)
    df_products.to_csv(os.path.join(DATA_PROCESSED_DIR, "products_clean.csv"), index=False)
    print("✓ Saved cleaned dimension CSVs to data/processed/")

    print("\n✅ Data Generation Complete!")

if __name__ == "__main__":
    main()
