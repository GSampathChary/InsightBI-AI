# Enterprise-scale data approach

The web dashboard is designed to display **aggregated report data**, not raw operational tables. A chart should receive a few months, regions, or top products—not millions of transactions.

## What is implemented now

- Dashboard report bundles are cached for 60 seconds and automatically invalidated when a processed dataset changes.
- The dashboard exposes dataset size, source, and refresh status to users.
- Customer segment requests are paginated (`limit` and `offset`); an API response is capped at 500 rows.
- Product and regional reports are summary-level aggregates.

## Recommended production architecture

For large company data, load source systems into PostgreSQL, Snowflake, BigQuery, or a data lake—not a browser-uploaded CSV. Build a scheduled ETL job that validates and transforms data into fact and dimension tables. Add materialized aggregate tables for daily/monthly metrics, then point the API at those aggregates.

Use a worker queue for imports and ML jobs, Redis for shared caching, object storage for source files, and a load balancer with multiple API instances. Enforce tenant isolation, role-based access, audit logging, and row-level security before giving users access to customer-level records.

## User experience at scale

1. Users open a summary report that loads compact pre-aggregated data quickly.
2. They filter a report by date, geography, or business unit.
3. They drill into a paginated detail table only when needed.
4. Large refreshes run in the background and show a completion/failure notification rather than blocking the dashboard.

This keeps the site responsive while the reporting model can grow independently.
