# Power BI Portfolio Walkthrough

This guide helps a reviewer assess InsightBI AI as an end-to-end business intelligence project rather than as a collection of dashboards.

## 1. The business question

The model answers four executive questions:

- Which regions, products, and customer segments create profitable growth?
- Where is revenue or margin trending away from plan?
- Which customers are valuable, loyal, or at risk of churn?
- What action should a sales or operations leader take next?

## 2. Data model

The project uses a Kimball-style star schema. `fact_sales` is the central transaction table, joined many-to-one to the Date, Customer, Product, and Region dimensions. Forecasts, customer RFM segments, anomalies, and generated insights are stored separately so that analytical outputs do not change the grain of the sales fact.

Use single-direction filters from dimensions to facts, mark `dim_date[date]` as the date table, and keep dimension keys hidden in the report view. This produces predictable filtering and avoids ambiguous relationship paths.

## 3. Load and refresh

1. Run the ETL pipeline or load the supplied CSV files from `data/processed`.
2. In Power Query, use the reusable calendar query in `powerbi/power_query_scripts.m`.
3. Connect the fact and dimension tables to PostgreSQL for a production setup, or use the processed CSV files for a portable portfolio demo.
4. Disable load for staging queries, apply types before merges, and filter unused columns at the source.
5. Refresh the model and validate row counts, total revenue, and total profit against the FastAPI dashboard.

## 4. Measures worth showing in a review

```dax
Total Revenue = SUM(fact_sales[revenue])

Total Profit = SUM(fact_sales[profit])

Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)

Orders = DISTINCTCOUNT(fact_sales[order_id])

Average Order Value = DIVIDE([Total Revenue], [Orders], 0)

Revenue MoM % =
VAR PreviousMonthRevenue =
    CALCULATE([Total Revenue], DATEADD(dim_date[date], -1, MONTH))
RETURN
    DIVIDE([Total Revenue] - PreviousMonthRevenue, PreviousMonthRevenue)
```

Format revenue and profit as Indian Rupees (`₹ #,##0`), percentages as percentages, and counts as whole numbers using the Indian digit grouping convention. Measures—not calculated columns—should perform aggregations so visuals remain responsive as data grows.

## 5. Recommended report pages

| Page | Audience | Core visuals | Decision supported |
| --- | --- | --- | --- |
| Executive overview | Leadership | KPI cards, monthly revenue/profit trend, insight cards | Is performance healthy and where should attention go? |
| Sales and regions | Sales leadership | Revenue/profit by Indian region, state ranking, month trend | Which territory should receive investment? |
| Customers | Growth and retention | RFM segment distribution, customer roster, recency trend | Who should be retained or reactivated? |
| Products | Merchandising | Top products, category margin, Pareto contribution | Which products should be promoted or reviewed? |
| Forecast and risk | Operations | Actual versus forecast, anomaly table, confidence bounds | Where is intervention needed before results deteriorate? |

Keep a consistent Power BI visual hierarchy: KPIs first, a trend second, drivers third, and a detailed table last. Use accessible labels, sufficient contrast, descriptive titles, and report-page tooltips for metric definitions.

## 6. Validation checklist

Before sharing the `.pbix` file, confirm:

- `fact_sales` has the expected transaction grain: one row per sales line.
- Date, Customer, Product, and Region relationships are active and many-to-one.
- KPI totals reconcile to the processed sales dataset.
- Slicers filter every relevant visual, including tooltips.
- Empty states are explicit; sample data is labelled as a demo, never presented as live production data.
- Refresh credentials and secrets are not embedded in the report file or repository.

## 7. Five-minute reviewer demo

1. Start on **Executive overview** and state the current revenue, profit margin, and month-over-month trend.
2. Select a region to demonstrate cross-filtering from the overview to the sales page.
3. Open **Customers** and explain how RFM prioritizes a retention action.
4. Open **Products** and compare revenue contribution with margin—not revenue alone.
5. Finish on **Forecast and risk** to show how anomaly detection turns descriptive BI into operational action.

The web dashboard at `/dashboard` mirrors this story for reviewers who cannot open Power BI Desktop. It is a companion experience; the PBIX file and documented model remain the primary Power BI artifact.
