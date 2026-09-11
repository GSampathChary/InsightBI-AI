"""
InsightBI AI — Copilot REST Endpoint (backend/app/api/v1/copilot.py)
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from ai_copilot.nl_to_sql import convert_nl_to_sql
from ai_copilot.insight_narrator import narrate_insights
from backend.app.services.analytics_service import get_analytics_summary

router = APIRouter()

class CopilotQueryRequest(BaseModel):
    query: str

class CopilotQueryResponse(BaseModel):
    query: str
    sql: str
    summary: str
    key_takeaways: List[str]
    recommended_chart: str
    data_preview: List[Dict[str, Any]]

@router.post("/query", response_model=CopilotQueryResponse)
def copilot_query(request: CopilotQueryRequest):
    """Processes natural-language query, generates SQL, returns executive summary and chart recommendation."""
    nl_res = convert_nl_to_sql(request.query)
    sql = nl_res.get("generated_sql", "")

    summary_bundle = get_analytics_summary()
    narrative = narrate_insights(request.query, sql, summary_bundle.get("trends", []))

    preview_data = summary_bundle.get("trends", [])[:5]

    return {
        "query": request.query,
        "sql": sql,
        "summary": narrative.get("summary", ""),
        "key_takeaways": narrative.get("key_takeaways", []),
        "recommended_chart": narrative.get("recommended_chart", "line_chart"),
        "data_preview": preview_data
    }
