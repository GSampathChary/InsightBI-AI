from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class SalesAnomaly(Base):
    __tablename__ = "sales_anomalies"

    anomaly_id = Column(Integer, primary_key=True, index=True)
    date_id = Column(Integer, ForeignKey("dim_date.date_id"), nullable=False)
    metric = Column(String(50), nullable=False)
    actual_value = Column(Numeric(12, 2), nullable=False)
    expected_value = Column(Numeric(12, 2), nullable=False)
    anomaly_score = Column(Numeric(8, 4), nullable=False)
    severity = Column(String(20), nullable=False)
    explanation = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
