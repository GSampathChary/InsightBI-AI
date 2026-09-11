import pytest
from fastapi.testclient import TestClient
from ai_copilot.nl_to_sql import convert_nl_to_sql, NLToSQLEngine
from ai_copilot.insight_narrator import narrate_insights
from backend.app.main import app

client = TestClient(app)

def test_nl_to_sql_conversion():
    res = convert_nl_to_sql("What is total revenue by product?")
    assert res["success"] is True
    assert "SELECT" in res["generated_sql"]
    assert "fact_sales" in res["generated_sql"] or "dim_product" in res["generated_sql"]

def test_sql_safety_sanitizer():
    engine = NLToSQLEngine()
    # 1. Valid SELECT
    assert engine.sanitize_sql("SELECT * FROM fact_sales") == "SELECT * FROM fact_sales;"

    # 2. Invalid DROP query
    with pytest.raises(ValueError) as exc:
        engine.sanitize_sql("DROP TABLE fact_sales")
    assert "Security Alert" in str(exc.value)

def test_insight_narrator():
    res = narrate_insights("What was our top revenue region?", "SELECT * FROM dim_region")
    assert "summary" in res
    assert "key_takeaways" in res
    assert len(res["key_takeaways"]) > 0

def test_copilot_api_endpoint():
    payload = {"query": "Show monthly sales trend"}
    response = client.post("/api/v1/copilot/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "Show monthly sales trend"
    assert "SELECT" in data["sql"]
    assert "summary" in data
    assert "recommended_chart" in data
