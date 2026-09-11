-- InsightBI AI — Database Schema: 02_fact_tables.sql

-- -----------------------------------------------------------------------------
-- 1. fact_sales: Core Sales Transaction Fact Table
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_id BIGSERIAL PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    date_id INT NOT NULL REFERENCES dim_date(date_id),
    customer_id INT NOT NULL REFERENCES dim_customer(customer_id),
    product_id INT NOT NULL REFERENCES dim_product(product_id),
    region_id INT NOT NULL REFERENCES dim_region(region_id),
    employee_id INT REFERENCES dim_employee(employee_id),
    campaign_id INT REFERENCES dim_campaign(campaign_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    unit_cost NUMERIC(10, 2) NOT NULL CHECK (unit_cost >= 0),
    discount NUMERIC(5, 4) NOT NULL DEFAULT 0.0000 CHECK (discount >= 0 AND discount <= 1),
    revenue NUMERIC(12, 2) NOT NULL,
    cost NUMERIC(12, 2) NOT NULL,
    profit NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 2. fact_forecast: Sales Forecast Predictions Fact Table
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_forecast (
    forecast_id SERIAL PRIMARY KEY,
    date_id INT NOT NULL REFERENCES dim_date(date_id),
    forecast_date DATE NOT NULL,
    predicted_revenue NUMERIC(12, 2) NOT NULL,
    lower_bound NUMERIC(12, 2) NOT NULL,
    upper_bound NUMERIC(12, 2) NOT NULL,
    model_name VARCHAR(50) NOT NULL DEFAULT 'XGBoost_TimeSeries',
    model_version VARCHAR(20) NOT NULL DEFAULT 'v1.0',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 3. fact_customer_activity: Web & Store Customer Engagement
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_customer_activity (
    activity_id BIGSERIAL PRIMARY KEY,
    date_id INT NOT NULL REFERENCES dim_date(date_id),
    customer_id INT NOT NULL REFERENCES dim_customer(customer_id),
    activity_type VARCHAR(50) NOT NULL, -- e.g., PageView, AddToCart, SupportTicket, Return
    session_duration INT DEFAULT 0,
    pages_viewed INT DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 4. fact_marketing: Campaign Regional Metrics Fact Table
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_marketing (
    marketing_id SERIAL PRIMARY KEY,
    date_id INT NOT NULL REFERENCES dim_date(date_id),
    campaign_id INT NOT NULL REFERENCES dim_campaign(campaign_id),
    region_id INT NOT NULL REFERENCES dim_region(region_id),
    impressions INT NOT NULL DEFAULT 0,
    clicks INT NOT NULL DEFAULT 0,
    spend NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    conversions INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 5. customer_segments: RFM Analytics Output Table
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customer_segments (
    segment_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL UNIQUE REFERENCES dim_customer(customer_id),
    recency_days INT NOT NULL,
    frequency_count INT NOT NULL,
    monetary_value NUMERIC(12, 2) NOT NULL,
    r_score INT NOT NULL,
    f_score INT NOT NULL,
    m_score INT NOT NULL,
    rfm_score INT NOT NULL,
    rfm_segment VARCHAR(50) NOT NULL, -- VIP, Loyal, At-Risk, Churned, etc.
    cluster_id INT NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 6. sales_anomalies: Outlier & Anomaly Detection Log Table
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sales_anomalies (
    anomaly_id SERIAL PRIMARY KEY,
    date_id INT NOT NULL REFERENCES dim_date(date_id),
    metric VARCHAR(50) NOT NULL, -- Revenue, Orders, Margin
    actual_value NUMERIC(12, 2) NOT NULL,
    expected_value NUMERIC(12, 2) NOT NULL,
    anomaly_score NUMERIC(8, 4) NOT NULL,
    severity VARCHAR(20) NOT NULL, -- High, Medium, Low
    explanation TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 7. business_insights: Automated Business Insights Log
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS business_insights (
    insight_id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL, -- Growth, Risk, Opportunity, Product, Customer
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    metric_impact VARCHAR(100),
    severity VARCHAR(20) NOT NULL DEFAULT 'Info',
    recommendation TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 8. ai_queries: LLM Copilot Interaction Log Table
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ai_queries (
    query_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    question TEXT NOT NULL,
    intent VARCHAR(50),
    generated_query TEXT,
    response TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
