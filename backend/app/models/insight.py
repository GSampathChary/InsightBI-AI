from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class BusinessInsight(Base):
    __tablename__ = "business_insights"

    insight_id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    metric_impact = Column(String(100), nullable=True)
    severity = Column(String(20), default="Info")
    recommendation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AIQuery(Base):
    __tablename__ = "ai_queries"

    query_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    question = Column(Text, nullable=False)
    intent = Column(String(50), nullable=True)
    generated_query = Column(Text, nullable=True)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
