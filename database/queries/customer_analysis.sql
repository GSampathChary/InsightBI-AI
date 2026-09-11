-- InsightBI AI — Analytical SQL: customer_analysis.sql

-- 1. Customer RFM Metrics Aggregation
SELECT
    c.customer_id,
    c.customer_code,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.customer_segment,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.revenue) AS total_spent,
    ROUND(AVG(f.revenue), 2) AS avg_order_value,
    MAX(d.date) AS last_order_date,
    CURRENT_DATE - MAX(d.date) AS recency_days
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY c.customer_id, c.customer_code, c.first_name, c.last_name, c.customer_segment
ORDER BY total_spent DESC;

-- 2. Customer Repeat Order Rate Breakdown
WITH customer_order_counts AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM fact_sales
    GROUP BY customer_id
)
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(
        (SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END)::NUMERIC / COUNT(*)) * 100, 2
    ) AS repeat_purchase_rate_percent
FROM customer_order_counts;
