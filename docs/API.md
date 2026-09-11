# REST API Reference & OpenAPI Specification

## Base URL
`http://localhost:8000/api/v1`

---

## Endpoints

### 1. Authentication (`/auth`)
- `POST /auth/register`: Register new user account.
- `POST /auth/login`: Authenticate and receive JWT access token.
- `POST /auth/refresh`: Issue new access token using refresh token.
- `GET /auth/me`: Retrieve current user profile and role.

### 2. Executive Dashboard (`/dashboard`)
- `GET /dashboard/summary`: High-level KPI metrics summary.
- `GET /dashboard/trends`: Time-series monthly revenue and profit trends.

### 3. Analytics & ML (`/analytics`)
- `GET /analytics/forecast`: Retrieve 30-day sales forecast predictions.
- `GET /analytics/segments`: Retrieve customer RFM segmentation clusters.
- `GET /analytics/anomalies`: Retrieve detected sales anomalies.

### 4. AI Copilot (`/copilot`)
- `POST /copilot/query`: Process natural-language query, generate SQL, and return executive narrative summary.

### 5. Reports & Exports (`/reports`)
- `GET /reports/pdf`: Download executive PDF report.
- `GET /reports/csv`: Download CSV analytics package.
- `POST /reports/schedule`: Schedule automated report generation.
