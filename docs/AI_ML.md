# Machine Learning Engine & AI Copilot Technical Guide

## Machine Learning Engine (`ml/`)

### 1. Sales Forecasting (`ml/models/sales_forecaster.py`)
- **Algorithm**: `RandomForestRegressor(n_estimators=100, random_state=42)`
- **Features**: Lagged revenue, month index, quarter, rolling 7-day mean.
- **Output**: 30-day ahead revenue forecast per territory.

### 2. Customer RFM Segmentation (`ml/models/customer_segmenter.py`)
- **Algorithm**: `KMeans(n_clusters=4, random_state=42)`
- **Features**:
  - **Recency (R)**: Days since last order.
  - **Frequency (F)**: Total order count.
  - **Monetary (M)**: Cumulative dollar spend.
- **Segments**: `VIP / Champions`, `Loyal Customers`, `Potential Loyalists`, `At-Risk / Lost`.

### 3. Anomaly Detection (`ml/models/anomaly_detector.py`)
- **Algorithm**: `IsolationForest(contamination=0.05, random_state=42)`
- **Features**: Order quantity, total revenue, unit price deviation.

---

## AI Copilot Engine (`ai_copilot/`)

### Architecture & Safety Flow
1. User enters natural language question (e.g., "Show me sales by region").
2. LLM Client evaluates question against database schema schema dictionary.
3. SQL Sanitizer validates SQL string to ensure NO destructive commands (`DROP`, `DELETE`, `UPDATE`, `ALTER`, `TRUNCATE`, `INSERT`).
4. System executes SQL query against PostgreSQL data warehouse and formats result table.
5. Insight Narrator produces executive summary text and key business takeaways.
