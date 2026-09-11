# Power BI & DAX Business Metrics Handbook

## Overview
The InsightBI AI platform provides production Power BI data model definitions, Power Query M data cleaning scripts, and DAX business measures.

---

## Power Query M Data Import Script
```m
let
    Source = PostgreSQL.Database("localhost", "insightbi_dw"),
    dbo_fact_sales = Source{[Schema="public",Item="fact_sales"]}[Data]
in
    dbo_fact_sales
```

---

## DAX Measure Glossary

### 1. Financial Metrics
- **Total Revenue**:
  ```dax
  Total Revenue = SUM(fact_sales[total_revenue])
  ```
- **Total Cost**:
  ```dax
  Total Cost = SUM(fact_sales[total_cost])
  ```
- **Total Profit**:
  ```dax
  Total Profit = [Total Revenue] - [Total Cost]
  ```
- **Profit Margin %**:
  ```dax
  Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0) * 100
  ```

### 2. Customer Metrics
- **Average Order Value (AOV)**:
  ```dax
  Average Order Value = DIVIDE([Total Revenue], DISTINCTCOUNT(fact_sales[sales_id]), 0)
  ```
- **Active Customer Count**:
  ```dax
  Active Customers = DISTINCTCOUNT(fact_sales[customer_id])
  ```
