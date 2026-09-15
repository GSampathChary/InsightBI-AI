# InsightBI AI — Power BI Data Warehouse & Dashboard Architecture

## 1. Star-Schema Data Model Overview

InsightBI AI relies on a clean, high-performance **Star-Schema** data model optimized for Power BI aggregation performance and DAX measure evaluation.

```
       +-------------------+
       |     dim_date      |
       +-------------------+
                 | 1
                 |
                 | *
+------------------------------------+       +---------------------+
|             fact_sales             |----1--|    dim_customer     |
+------------------------------------+       +---------------------+
  * |            * |          * |
    | 1            | 1          | 1
+---------+   +----------+   +----------+
|dim_prod |   |dim_region|   |dim_employ|
+---------+   +----------+   +----------+
```

### Relationships Specification
1. `dim_date[date_id]` (1) ─── (*) `fact_sales[date_id]` (Single direction filter, `dim_date` filters `fact_sales`)
2. `dim_customer[customer_id]` (1) ─── (*) `fact_sales[customer_id]` (Single direction filter)
3. `dim_product[product_id]` (1) ─── (*) `fact_sales[product_id]` (Single direction filter)
4. `dim_region[region_id]` (1) ─── (*) `fact_sales[region_id]` (Single direction filter)
5. `dim_employee[employee_id]` (1) ─── (*) `fact_sales[employee_id]` (Single direction filter)

---

## 2. Power BI DirectQuery vs Import Mode Strategy

- **Import Mode (Recommended for < 10M rows)**:
  - In-memory VertiPaq engine compression delivers sub-second DAX evaluation speed.
  - Scheduled refresh 4x/day via Gateway or automated API sync.
- **DirectQuery / Hybrid Mode (Enterprise Scale > 10M rows)**:
  - Fact table `fact_sales` in DirectQuery mode linked to in-memory dimension tables (Dual mode).

---

## 3. Row-Level Security (RLS) Design

Three security roles are defined:
1. `RegionalManagerRole`:
   ```dax
   [region_id] = LOOKUPVALUE(users[region_id], users[email], USERPRINCIPALNAME())
   ```
2. `ExecutiveRole`:
   - Full unfiltered access across all regions and metric types.
3. `AnalystRole`:
   - Masked customer PII (phone number and exact address hidden).

---

## 4. Power BI 5-Page Dashboard Specification

### Page 1: Executive Overview
- **Header KPIs**: Total Revenue, Total Profit, Profit Margin %, Total Orders, AOV.
- **Visuals**:
  - Line Chart: Monthly Revenue & Profit Trend (with YoY growth toggle).
  - Donut Chart: Revenue Breakdown by Product Category.
  - Map Visual: Regional Revenue Density across Indian states.
  - KPI Cards: Top Performing Region & Top Selling SKU.

### Page 2: Sales Performance & Financial Analytics
- **Header KPIs**: YTD Revenue, Prior Year Revenue, YoY Growth %, MoM Growth %.
- **Visuals**:
  - Waterfall Chart: Month-over-Month Revenue Delta.
  - Bar Chart: Discount vs Profit Margin Impact by Subcategory.
  - Matrix Table: Sales Representative Leaderboard (Revenue, Orders, Commission).

### Page 3: Customer Segmentation & RFM Analytics
- **Header KPIs**: Total Customers, Repeat Customer Count, Retention Rate %, Customer Lifetime Value (CLV).
- **Visuals**:
  - Scatter Plot: Recency vs Monetary Value per Customer.
  - Treemap: Customer RFM Segments (VIP, Champions, At-Risk, Lost).
  - Bar Chart: Average Order Frequency by Customer Segment.

### Page 4: Product Analytics & Inventory
- **Header KPIs**: Active Product Count, Top Category Revenue, Avg Unit Cost, Avg Unit Price.
- **Visuals**:
  - Bar Chart: Top 10 Best Selling Products by Revenue.
  - Bar Chart: Bottom 10 Products by Profit Margin.
  - Table: Product Catalog Master Table with SKU search slicer.

### Page 5: Regional & Territory Intelligence
- **Header KPIs**: Total Regions, Top Territory Revenue, Regional Profit Margin %.
- **Visuals**:
  - Filled Map: State-by-State Profitability Heatmap.
  - Bar Chart: Territory Revenue vs Cost Breakdown.
