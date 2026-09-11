-- InsightBI AI — Analytical SQL: sales_analysis.sql

-- 1. Monthly Revenue, Profit, and Month-over-Month (MoM) Revenue Growth %
WITH monthly_sales AS (
    SELECT
        d.year,
        d.month,
        d.month_name,
        SUM(f.revenue) AS total_revenue,
        SUM(f.profit) AS total_profit,
        COUNT(DISTINCT f.order_id) AS total_orders,
        COUNT(DISTINCT f.customer_id) AS total_customers
    FROM fact_sales f
    JOIN dim_date d ON f.date_id = d.date_id
    GROUP BY d.year, d.month, d.month_name
)
SELECT
    year,
    month,
    month_name,
    total_revenue,
    total_profit,
    total_orders,
    total_customers,
    ROUND((total_profit / NULLIF(total_revenue, 0)) * 100, 2) AS profit_margin_percent,
    ROUND(
        ((total_revenue - LAG(total_revenue) OVER (ORDER BY year, month)) / 
        NULLIF(LAG(total_revenue) OVER (ORDER BY year, month), 0)) * 100, 2
    ) AS mom_growth_percent
FROM monthly_sales
ORDER BY year, month;

-- 2. Regional Sales & Profitability Analysis
SELECT
    r.region_id,
    r.region_name,
    r.territory,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.revenue) AS total_revenue,
    SUM(f.profit) AS total_profit,
    ROUND(AVG(f.revenue), 2) AS avg_order_value,
    ROUND((SUM(f.profit) / NULLIF(SUM(f.revenue), 0)) * 100, 2) AS margin_percent
FROM fact_sales f
JOIN dim_region r ON f.region_id = r.region_id
GROUP BY r.region_id, r.region_name, r.territory
ORDER BY total_revenue DESC;
