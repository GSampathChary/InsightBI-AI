# Using InsightBI

InsightBI is organised like a report workspace: start on **Overview**, then move into a focused report when a metric needs investigation.

## The simple workflow

1. Select **Get data** in the top-right corner.
2. If needed, use **Download Template** in the import window to see the expected CSV columns.
3. Choose a CSV file, then select **Process & Update Dashboard**. The application validates and imports the data before refreshing reports.
4. Begin at **Overview** for revenue, profit, orders, customers, trend, and priority insights.
5. Use the left navigation to answer a more specific question:
   - **Sales**: territory revenue, profit, and order volume.
   - **Customers**: RFM customer segments and retention risk.
   - **Products**: top products and margin performance.
   - **Ask AI**: write a question in everyday language, for example: `Which region had the highest revenue?`

## Tips

- Use **Refresh** in the header to reload the current report when a pipeline or dataset update has completed.
- The dashboard uses sample values automatically when the API is unavailable, so the reporting experience remains explorable during local setup.
- CSV uploads currently support sales data with headers. The template is the quickest way to begin with a valid file.
