# PostgreSQL Data Warehouse & Star-Schema Specification

## Star Schema Overview
The InsightBI AI PostgreSQL data warehouse follows a Ralph Kimball dimensional modeling approach organized into 4 dimension tables and 1 central fact table.

```mermaid
erDiagram
    FACT_SALES }|--|| DIM_CUSTOMER : "purchased by"
    FACT_SALES }|--|| DIM_PRODUCT : "contains"
    FACT_SALES }|--|| DIM_REGION : "sold in"
    FACT_SALES }|--|| DIM_DATE : "ordered on"

    DIM_CUSTOMER {
        int customer_id PK
        string customer_name
        string email
        string segment
    }

    DIM_PRODUCT {
        int product_id PK
        string product_name
        string category
        decimal unit_price
        decimal unit_cost
    }

    DIM_REGION {
        int region_id PK
        string region_name
        string territory
        string country
    }

    DIM_DATE {
        int date_id PK
        date full_date
        int year
        int quarter
        int month
        string month_name
    }

    FACT_SALES {
        int sales_id PK
        int customer_id FK
        int product_id FK
        int region_id FK
        int date_id FK
        int quantity
        decimal unit_price
        decimal total_revenue
        decimal total_cost
        decimal net_profit
    }
```

---

## Table DDL Reference

```sql
-- Fact Sales Table
CREATE TABLE fact_sales (
    sales_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES dim_customer(customer_id),
    product_id INT REFERENCES dim_product(product_id),
    region_id INT REFERENCES dim_region(region_id),
    date_id INT REFERENCES dim_date(date_id),
    quantity INT NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    total_revenue NUMERIC(14, 2) NOT NULL,
    total_cost NUMERIC(14, 2) NOT NULL,
    net_profit NUMERIC(14, 2) NOT NULL
);

CREATE INDEX idx_fact_sales_date ON fact_sales(date_id);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_id);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_id);
```
