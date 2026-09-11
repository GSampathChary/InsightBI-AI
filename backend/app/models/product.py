from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class DimProduct(Base):
    __tablename__ = "dim_product"

    product_id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(30), unique=True, nullable=False, index=True)
    product_name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    subcategory = Column(String(50), nullable=False)
    unit_cost = Column(Numeric(10, 2), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    supplier = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
