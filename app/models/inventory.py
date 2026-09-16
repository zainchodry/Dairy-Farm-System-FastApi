from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base

class TxTypeEnum(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    item_type = Column(String) 
    unit_of_measure = Column(String)
    quantity_in_stock = Column(Numeric(10, 2), default=0.00)
    reorder_level = Column(Numeric(10, 2), default=10.00)

    transactions = relationship("StockTransaction", back_populates="item")

class StockTransaction(Base):
    __tablename__ = "stock_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"))
    transaction_type = Column(Enum(TxTypeEnum))
    quantity = Column(Numeric(10, 2))
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    handled_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    notes = Column(String, nullable=True)

    item = relationship("Item", back_populates="transactions")
    handled_by = relationship("User", back_populates="inventory_actions")