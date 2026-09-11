from sqlalchemy import Column, Integer, String, Date, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class DimDate(Base):
    __tablename__ = "dim_date"

    date_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, nullable=False, index=True)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    month_name = Column(String(15), nullable=False)
    week_of_year = Column(Integer, nullable=False)
    day_of_week = Column(Integer, nullable=False)
    day_name = Column(String(15), nullable=False)
    is_weekend = Column(Boolean, default=False, nullable=False)
    holiday = Column(Boolean, default=False, nullable=False)
    holiday_name = Column(String(50), nullable=True)

class DimRegion(Base):
    __tablename__ = "dim_region"

    region_id = Column(Integer, primary_key=True, index=True)
    region_name = Column(String(50), nullable=False)
    country = Column(String(50), default="United States", nullable=False)
    state = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    territory = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DimCustomer(Base):
    __tablename__ = "dim_customer"

    customer_id = Column(Integer, primary_key=True, index=True)
    customer_code = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(30), nullable=True)
    region_id = Column(Integer, ForeignKey("dim_region.region_id"))
    customer_segment = Column(String(50), default="Standard")
    credit_limit = Column(Numeric(12, 2), default=1000.00)
    registration_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CustomerSegment(Base):
    __tablename__ = "customer_segments"

    segment_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("dim_customer.customer_id"), unique=True, nullable=False)
    recency_days = Column(Integer, nullable=False)
    frequency_count = Column(Integer, nullable=False)
    monetary_value = Column(Numeric(12, 2), nullable=False)
    r_score = Column(Integer, nullable=False)
    f_score = Column(Integer, nullable=False)
    m_score = Column(Integer, nullable=False)
    rfm_score = Column(Integer, nullable=False)
    rfm_segment = Column(String(50), nullable=False)
    cluster_id = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
