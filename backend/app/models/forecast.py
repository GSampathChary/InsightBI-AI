from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class FactForecast(Base):
    __tablename__ = "fact_forecast"

    forecast_id = Column(Integer, primary_key=True, index=True)
    date_id = Column(Integer, ForeignKey("dim_date.date_id"), nullable=False)
    forecast_date = Column(Date, nullable=False, index=True)
    predicted_revenue = Column(Numeric(12, 2), nullable=False)
    lower_bound = Column(Numeric(12, 2), nullable=False)
    upper_bound = Column(Numeric(12, 2), nullable=False)
    model_name = Column(String(50), default="XGBoost_TimeSeries")
    model_version = Column(String(20), default="v1.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
