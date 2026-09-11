-- InsightBI AI — Analytical SQL: product_analysis.sql

-- 1. Top 10 Best Selling Products by Revenue
SELECT
    p.product_id,
    p.sku,
    p.product_name,
    p.category,
    p.subcategory,
    SUM(f.quantity) AS total_quantity_sold,
    SUM(f.revenue) AS total_revenue,
    SUM(f.profit) AS total_profit,
    ROUND((SUM(f.profit) / NULLIF(SUM(f.revenue), 0)) * 100, 2) AS margin_percent
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.product_id, p.sku, p.product_name, p.category, p.subcategory
ORDER BY total_revenue DESC
LIMIT 10;

-- 2. Category Level Profitability & Discount Impact
SELECT
    p.category,
    COUNT(DISTINCT f.product_id) AS active_products,
    SUM(f.quantity) AS total_units_sold,
    SUM(f.revenue) AS total_revenue,
    SUM(f.profit) AS total_profit,
    ROUND(AVG(f.discount) * 100, 2) AS avg_discount_percent,
    ROUND((SUM(f.profit) / NULLIF(SUM(f.revenue), 0)) * 100, 2) AS category_margin_percent
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
