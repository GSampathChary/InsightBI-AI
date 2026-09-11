# Data Dictionary — InsightBI AI

## Star-Schema Tables Overview

### Dimension Tables
- `dim_date`: Calendar dimension containing date, month, quarter, year, day_of_week, is_weekend, holiday.
- `dim_customer`: Customer details containing customer_id, name, email, region_id, customer_segment, registration_date.
- `dim_product`: Product catalog containing product_id, product_name, category, subcategory, unit_cost, unit_price.
- `dim_region`: Geographical hierarchy containing region_id, region_name, country, state, territory.
- `dim_employee`: Sales representative information.
- `dim_campaign`: Marketing campaign metadata.

### Fact & Analytics Tables
- `fact_sales`: Transactional facts containing sales_id, date_id, customer_id, product_id, region_id, employee_id, quantity, unit_price, discount, revenue, cost, profit.
- `fact_forecast`: Prediction facts containing forecast_id, forecast_date, predicted_revenue, lower_bound, upper_bound, model_name, model_version.
- `customer_segments`: RFM & K-Means output containing customer_id, recency_score, frequency_score, monetary_score, rfm_segment, cluster_id.
- `sales_anomalies`: Anomaly log containing anomaly_id, date, metric, actual_value, expected_value, anomaly_score, severity, explanation.
- `ai_queries`: System query history containing query_id, user_id, question, intent, generated_tool, response, created_at.
