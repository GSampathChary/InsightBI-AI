"""
InsightBI AI — Customer Endpoints (backend/app/api/v1/customers.py)
"""

import os
import pandas as pd
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

SAMPLE_SEGMENTS = [
    {"customer_id": 1, "customer_code": "CUST-000001", "first_name": "James", "last_name": "Smith", "email": "james.smith1@example.com", "recency_days": 12, "frequency_count": 28, "monetary_value": 14500.50, "r_score": 5, "f_score": 5, "m_score": 5, "rfm_score": 555, "rfm_segment": "VIP / Champions"},
    {"customer_id": 2, "customer_code": "CUST-000002", "first_name": "Jennifer", "last_name": "Johnson", "email": "jennifer.johnson2@example.com", "recency_days": 18, "frequency_count": 19, "monetary_value": 9820.00, "r_score": 5, "f_score": 4, "m_score": 4, "rfm_score": 544, "rfm_segment": "VIP / Champions"},
    {"customer_id": 3, "customer_code": "CUST-000003", "first_name": "Robert", "last_name": "Williams", "email": "robert.williams3@example.com", "recency_days": 35, "frequency_count": 14, "monetary_value": 6450.25, "r_score": 4, "f_score": 4, "m_score": 4, "rfm_score": 444, "rfm_segment": "Loyal Customers"},
    {"customer_id": 4, "customer_code": "CUST-000004", "first_name": "Sarah", "last_name": "Brown", "email": "sarah.brown4@example.com", "recency_days": 42, "frequency_count": 11, "monetary_value": 4890.00, "r_score": 3, "f_score": 3, "m_score": 3, "rfm_score": 333, "rfm_segment": "Potential Loyalists"},
    {"customer_id": 5, "customer_code": "CUST-000005", "first_name": "Michael", "last_name": "Jones", "email": "michael.jones5@example.com", "recency_days": 95, "frequency_count": 3, "monetary_value": 850.00, "r_score": 1, "f_score": 1, "m_score": 1, "rfm_score": 111, "rfm_segment": "At-Risk / Lost"}
]

@router.get("/segments")
def get_customer_segments(
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    """Return one page only—never ship a full enterprise customer table to the browser."""
    filepath = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data", "processed", "customer_segments.csv")
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            if not df.empty:
                return df.iloc[offset:offset + limit].to_dict(orient="records")
        except Exception:
            pass
    return SAMPLE_SEGMENTS[offset:offset + limit]

@router.get("/{customer_id}")
def get_customer_details(customer_id: int):
    filepath = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data", "processed", "customer_segments.csv")
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            cust = df[df["customer_id"] == customer_id]
            if not cust.empty:
                return cust.iloc[0].to_dict()
        except Exception:
            pass
    for item in SAMPLE_SEGMENTS:
        if item["customer_id"] == customer_id:
            return item
    raise HTTPException(status_code=404, detail="Customer not found")
