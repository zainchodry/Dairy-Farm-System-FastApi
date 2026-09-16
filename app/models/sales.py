from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base

class PaymentEnum(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String, unique=True, index=True)
    address = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    purchases = relationship("MilkSale", back_populates="customer")

class MilkSale(Base):
    __tablename__ = "milk_sales"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"))
    sold_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    quantity_liters = Column(Numeric(8, 2))
    price_per_liter = Column(Numeric(6, 2))
    total_amount = Column(Numeric(10, 2))
    payment_status = Column(Enum(PaymentEnum), default=PaymentEnum.PENDING)
    notes = Column(String, nullable=True)

    customer = relationship("Customer", back_populates="purchases")
    sold_by = relationship("User", back_populates="processed_sales")