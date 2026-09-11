# InsightBI AI — System Architecture & Design Specification

## Overview
**InsightBI AI** is an enterprise-grade AI-powered Business Intelligence & Analytics platform designed to deliver real-time operational metrics, predictive analytics, natural language query copilot, and automated business insight generation.

---

## High-Level Architecture Diagram

```mermaid
graph TD
    subgraph Data Sources
        A1[OLTP Operational Data] --> B1[ETL Data Pipeline]
    end

    subgraph Data Warehouse
        B1 --> C1[(PostgreSQL Star Schema DW)]
    end

    subgraph Analytical & ML Engine
        C1 --> D1[Analytics Engine]
        C1 --> D2[Scikit-Learn ML Models]
        D2 --> E1[Sales Forecast & RFM Segments]
    end

    subgraph AI Analytics Copilot
        C1 --> F1[Schema-Aware NL-to-SQL]
        F1 --> F2[LLM Client / Fallback]
        F2 --> F3[Insight Narrative Generator]
    end

    subgraph Access & API Layer
        D1 --> G1[FastAPI REST API v1]
        E1 --> G1
        F3 --> G1
        G1 --> H1[JWT Auth & RBAC Security]
    end

    subgraph Visualization Suite
        G1 --> I1[Next.js Dashboard UI]
        C1 --> I2[Power BI Dashboards]
    end
```

---

## Component Specifications

### 1. Data Ingestion & ETL Pipeline (`etl/`)
- Clean, standardize, and validate raw CSV and relational data.
- Enforce business rules, currency normalization, and surrogate key assignment.
- Hydrate PostgreSQL star-schema dimension and fact tables (`dim_customer`, `dim_product`, `dim_region`, `dim_date`, `fact_sales`).

### 2. Analytical Engine (`analytics/`)
- Calculates business metrics (Revenue, Profit, Profit Margin %, AOV, Customer Retention).
- Provides aggregated SQL views and time-series rollup functions.

### 3. Machine Learning Engine (`ml/`)
- **Sales Forecasting**: `RandomForestRegressor` predicting 30-day regional and overall revenue.
- **Customer Segmentation**: `KMeans` RFM (Recency, Frequency, Monetary) clustering into 4 segments (VIP, Loyal, Potential, At-Risk).
- **Anomaly Detection**: `IsolationForest` detecting anomalous order volumes or transaction values.

### 4. AI Analytics Copilot (`ai_copilot/`)
- Converts natural-language questions to safe SQL queries.
- Includes strict regex query sanitizer blocking destructive SQL (`DROP`, `DELETE`, `UPDATE`, `ALTER`).
- Generates executive narrative summaries and actionable business takeaways.

### 5. FastAPI REST API (`backend/app/`)
- Production FastAPI framework with Pydantic request/response validation.
- JWT authentication, refresh token support, and Role-Based Access Control (`Admin`, `Executive`, `Analyst`, `Viewer`).

### 6. Next.js Frontend Dashboard (`frontend/`)
- Modern dark-themed dashboard built with Next.js App Router, TailwindCSS, and Recharts.
