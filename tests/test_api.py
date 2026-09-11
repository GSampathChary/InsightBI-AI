import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to InsightBI AI" in response.json()["message"]

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_auth_registration_and_login():
    # 1. Register User
    reg_payload = {
        "email": "analyst@insightbi.ai",
        "password": "SecurePassword123!",
        "full_name": "Senior Data Analyst",
        "role": "Analyst"
    }
    res_reg = client.post("/api/v1/auth/register", json=reg_payload)
    assert res_reg.status_code == 201
    assert res_reg.json()["email"] == "analyst@insightbi.ai"

    # 2. Login User
    login_payload = {
        "email": "analyst@insightbi.ai",
        "password": "SecurePassword123!"
    }
    res_login = client.post("/api/v1/auth/login", json=login_payload)
    assert res_login.status_code == 200
    token = res_login.json()["access_token"]
    assert token is not None

    # 3. Get /auth/me with Bearer token
    headers = {"Authorization": f"Bearer {token}"}
    res_me = client.get("/api/v1/auth/me", headers=headers)
    assert res_me.status_code == 200
    assert res_me.json()["email"] == "analyst@insightbi.ai"

def test_dashboard_summary_endpoint():
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert "kpis" in data
    assert "trends" in data
    assert "business_insights" in data

def test_sales_overview_endpoint():
    response = client.get("/api/v1/sales/overview")
    assert response.status_code == 200
    assert "kpis" in response.json()

def test_analytics_endpoints():
    res_forecast = client.get("/api/v1/analytics/forecast")
    assert res_forecast.status_code == 200

    res_insights = client.get("/api/v1/analytics/insights")
    assert res_insights.status_code == 200
