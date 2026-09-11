import pandas as pd
import pytest
from ml.forecasting.train_forecaster import train_sales_forecaster
from ml.segmentation.cluster_customers import train_customer_segmentation
from ml.anomalies.detect_anomalies import detect_sales_anomalies

def test_sales_forecaster_training():
    dates = pd.date_range("2024-01-01", periods=100)
    df_sales = pd.DataFrame({
        "date": dates,
        "revenue": [1000 + i * 10 + (i % 7) * 50 for i in range(100)]
    })
    res = train_sales_forecaster(df_sales, forecast_days=30)
    assert "forecast" in res
    assert len(res["forecast"]) == 30
    assert res["forecast"][0]["predicted_revenue"] > 0

def test_customer_segmentation_clustering():
    df_sales = pd.DataFrame([
        {"customer_id": 1, "order_id": f"O-{i}", "revenue": 100.0, "date_id": 20240101 + i} for i in range(10)
    ] + [
        {"customer_id": 2, "order_id": "O-20", "revenue": 5000.0, "date_id": 20240115}
    ])
    df_segments = train_customer_segmentation(df_sales)
    assert not df_segments.empty
    assert "rfm_segment" in df_segments.columns
    assert "cluster_id" in df_segments.columns
    assert len(df_segments) == 2

def test_anomaly_detection_isolation_forest():
    dates = pd.date_range("2024-01-01", periods=50)
    revenues = [1000.0] * 49 + [50000.0] # Massive spike on day 50
    df_sales = pd.DataFrame({
        "date": dates,
        "date_id": [int(d.strftime("%Y%m%d")) for d in dates],
        "revenue": revenues,
        "order_id": [f"ORD-{i}" for i in range(50)],
        "profit": [r * 0.4 for r in revenues]
    })

    df_anomalies = detect_sales_anomalies(df_sales)
    assert not df_anomalies.empty
    assert "severity" in df_anomalies.columns
