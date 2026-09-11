"""
InsightBI AI — Analytics Schemas (backend/app/schemas/analytics.py)
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ForecastItem(BaseModel):
    date: str
    date_id: int
    predicted_revenue: float
    lower_bound: float
    upper_bound: float
    model_name: str
    model_version: str

class ForecastResponse(BaseModel):
    forecast: List[ForecastItem]
    metrics: Dict[str, Any]

class CustomerSegmentItem(BaseModel):
    customer_id: int
    recency_days: int
    frequency_count: int
    monetary_value: float
    r_score: int
    f_score: int
    m_score: int
    rfm_score: int
    rfm_segment: str
    cluster_id: int

class AnomalyItem(BaseModel):
    date_id: int
    metric: str
    actual_value: float
    expected_value: float
    anomaly_score: float
    severity: str
    explanation: str

class BusinessInsightItem(BaseModel):
    category: str
    title: str
    description: str
    metric_impact: str
    severity: str
    recommendation: str
