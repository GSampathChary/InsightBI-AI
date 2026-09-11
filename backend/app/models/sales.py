from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime, ForeignKey, BigInteger
from sqlalchemy.sql import func
from app.core.database import Base

class FactSales(Base):
    __tablename__ = "fact_sales"

    sales_id = Column(BigInteger, primary_key=True, index=True)
    order_id = Column(String(50), nullable=False, index=True)
    date_id = Column(Integer, ForeignKey("dim_date.date_id"), nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("dim_customer.customer_id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("dim_product.product_id"), nullable=False, index=True)
    region_id = Column(Integer, ForeignKey("dim_region.region_id"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("dim_employee.employee_id"), nullable=True)
    campaign_id = Column(Integer, ForeignKey("dim_campaign.campaign_id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    unit_cost = Column(Numeric(10, 2), nullable=False)
    discount = Column(Numeric(5, 4), default=0.0000, nullable=False)
    revenue = Column(Numeric(12, 2), nullable=False)
    cost = Column(Numeric(12, 2), nullable=False)
    profit = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DimEmployee(Base):
    __tablename__ = "dim_employee"

    employee_id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(50), default="Sales Representative")
    region_id = Column(Integer, ForeignKey("dim_region.region_id"))
    hire_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

class DimCampaign(Base):
    __tablename__ = "dim_campaign"

    campaign_id = Column(Integer, primary_key=True, index=True)
    campaign_name = Column(String(100), nullable=False)
    channel = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    budget = Column(Numeric(12, 2), default=0.00)
