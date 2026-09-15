# InsightBI AI — AI-Powered Business Intelligence & Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-13+-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

**InsightBI AI** is an enterprise-grade, end-to-end AI-powered Business Intelligence & Analytics platform. It transforms raw business transaction data into clean analytical datasets, PostgreSQL star-schema data warehouse, Power BI dashboards, machine learning forecasts, RFM customer segmentations, automated PDF/CSV executive reports, and an interactive natural-language AI Analytics Copilot.

---

## 🌟 Key Platform Capabilities

### 1. Data Engineering & Star-Schema Data Warehouse
- **Automated Data Generators & Cleaning**: Synthetic transactional data generator producing 10,000+ orders across customers, products, and regional sales territories.
- **Dimensional Modeling**: Ralph Kimball star-schema structure (`dim_customer`, `dim_product`, `dim_region`, `dim_date`, `fact_sales`).
- **ETL Pipeline**: Idempotent data ingestion pipeline with validation, currency normalization, and automated table hydration.

### 2. Analytical Engine & Power BI Business Metrics
- High-performance analytics engine calculating Revenue, Net Profit, Profit Margin %, AOV, MoM Growth Rate, and Customer Retention.
- Power BI integration scripts including DAX metric measure handbook and Power Query M transform scripts.

### 3. Machine Learning Engine
- **Sales Forecasting**: `RandomForestRegressor` predicting 30-day regional revenue trends.
- **Customer RFM Segmentation**: `KMeans` clustering into 4 distinct segments (VIP / Champions, Loyal, Potential Loyalists, At-Risk / Lost).
- **Anomaly Detection**: `IsolationForest` detecting anomalous order volumes or transaction values.

### 4. AI Analytics Copilot
- Natural language query assistant converting plain English questions into safe SQL queries.
- SQL query sanitizer blocking destructive SQL (`DROP`, `DELETE`, `UPDATE`, `ALTER`, `TRUNCATE`).
- Executive narrative summary generator producing actionable business takeaways.

### 5. Production Next.js Dashboard Suite
- Dark-themed executive dashboard UI (`frontend/`) built with Next.js, React, TailwindCSS, and Recharts.
- 5 comprehensive views: Executive Overview, Sales Analytics, Customer RFM, Product Performance, and AI Copilot.

### 6. Enterprise Security & Reporting
- Role-Based Access Control (RBAC) supporting `Admin`, `Executive`, `Analyst`, and `Viewer` roles.
- Security audit log module (`logs/security_audit.log`).
- Automated PDF report exporter and CSV summary packager.

---

## 🏗️ Architecture Diagram

```mermaid
graph TD
    subgraph Data Sources & Ingestion
        A1[Raw Transaction Data] --> B1[ETL Data Pipeline]
    end

    subgraph Data Warehouse
        B1 --> C1[(PostgreSQL Star Schema DW)]
    end

    subgraph Analytics & ML Engine
        C1 --> D1[Analytics Engine]
        C1 --> D2[ML Models: Forecasting & RFM]
    end

    subgraph AI Copilot Engine
        C1 --> E1[NL-to-SQL Engine]
        E1 --> E2[Insight Narrator]
    end

    subgraph REST API & Security
        D1 --> F1[FastAPI REST API v1]
        D2 --> F1
        E2 --> F1
        F1 --> G1[JWT Auth & RBAC Security]
    end

    subgraph Frontend & Power BI
        G1 --> H1[Next.js Dashboard UI]
        C1 --> H2[Power BI Dashboards]
    end
```

---

## ⚡ Quickstart Guide

### 1. Run Master Unit Test Suite
```bash
python scripts/run_all_tests.py
```

### 2. Start Local Development Environment
- **FastAPI Backend**:
  ```bash
  uvicorn backend.app.main:app --reload --port 8000
  ```
- **Next.js Frontend**:
  ```bash
  cd frontend
  npm run dev
  ```

### 3. Deploy via Docker Compose
```bash
docker-compose up -d --build
python scripts/verify_deployment.py
```

---

## 📖 Technical Documentation

- 📐 [System Architecture Guide](docs/architecture.md)
- 🗄️ [Data Warehouse & Schema Reference](docs/DATABASE.md)
- 📊 [Power BI & DAX Metrics Handbook](docs/POWER_BI.md)
- 🎯 [Power BI Portfolio Walkthrough](docs/POWER_BI_PORTFOLIO_GUIDE.md)
- 🤖 [Machine Learning & AI Copilot Technical Guide](docs/AI_ML.md)
- 🔌 [REST API Reference Guide](docs/API.md)
- 🐳 [Docker & Production Deployment Guide](docs/deployment.md)

---

## 📜 License & Author
- **Author**: Senior Data & AI Architect
- **License**: MIT License
