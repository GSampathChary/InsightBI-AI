# Docker & Production Deployment Operations Guide

## Overview
InsightBI AI includes a production-grade multi-container Docker infrastructure orchestrated using Docker Compose.

---

## Quickstart Deployment

```bash
# 1. Clone repository and navigate to root directory
cd InsightBI-AI

# 2. Copy environment template
cp .env.example .env

# 3. Build and launch multi-container stack
docker-compose up -d --build

# 4. Verify deployment health
python scripts/verify_deployment.py
```

---

## Container Architecture
- `insightbi_postgres` (`5432`): PostgreSQL 15 Data Warehouse.
- `insightbi_redis` (`6379`): Redis Cache.
- `insightbi_backend` (`8000`): FastAPI Python 3.10 production REST server.
- `insightbi_frontend` (`3000`): Next.js 18 production frontend dashboard.
