import os
import pandas as pd

def test_generated_datasets():
    data_raw = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    data_proc = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

    df_customers = pd.read_csv(os.path.join(data_raw, "customers.csv"))
    df_products = pd.read_csv(os.path.join(data_raw, "products.csv"))
    df_orders = pd.read_csv(os.path.join(data_raw, "orders.csv"))
    df_sales = pd.read_csv(os.path.join(data_proc, "sales_clean.csv"))

    print(f"✓ Customers count: {len(df_customers):,}")
    print(f"✓ Products count: {len(df_products):,}")
    print(f"✓ Orders count: {len(df_orders):,}")
    print(f"✓ Fact Sales count: {len(df_sales):,}")

    assert len(df_customers) >= 10000, "Should generate at least 10,000 customers"
    assert len(df_products) >= 500, "Should generate at least 500 products"
    assert len(df_orders) >= 100000, "Should generate at least 100,000 orders"
    assert len(df_sales) >= 100000, "Should generate at least 100,000 sales facts"

    # Validate financial sanity: profit = revenue - cost
    rev = df_sales["revenue"].sum()
    cost = df_sales["cost"].sum()
    profit = df_sales["profit"].sum()
    print(f"✓ Total Revenue: ${rev:,.2f}")
    print(f"✓ Total Profit:  ${profit:,.2f}")
    assert abs((rev - cost) - profit) < 1.0, "Revenue - Cost must equal Profit"

if __name__ == "__main__":
    test_generated_datasets()
