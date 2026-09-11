-- InsightBI AI — Database Schema: 03_indexes.sql

-- Foreign Key Indexes for Fact Tables
CREATE INDEX IF NOT EXISTS idx_fact_sales_date ON fact_sales(date_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer ON fact_sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product ON fact_sales(product_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_region ON fact_sales(region_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_employee ON fact_sales(employee_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_order ON fact_sales(order_id);

-- Analytical Search & Aggregation Indexes
CREATE INDEX IF NOT EXISTS idx_product_category ON dim_product(category, subcategory);
CREATE INDEX IF NOT EXISTS idx_customer_region ON dim_customer(region_id);
CREATE INDEX IF NOT EXISTS idx_customer_segment ON dim_customer(customer_segment);
CREATE INDEX IF NOT EXISTS idx_date_year_month ON dim_date(year, month);
CREATE INDEX IF NOT EXISTS idx_customer_segments_rfm ON customer_segments(rfm_segment);
CREATE INDEX IF NOT EXISTS idx_anomalies_date ON sales_anomalies(date_id, severity);
CREATE INDEX IF NOT EXISTS idx_forecast_date ON fact_forecast(forecast_date);
