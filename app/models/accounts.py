from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    VET = "VET"
    WORKER = "WORKER"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.WORKER)
    
    profile = relationship("Profile", back_populates="user", uselist=False)
    # Relationships to other modules (using string names avoids circular imports)
    milking_logs = relationship("MilkYield", back_populates="milked_by")
    diagnoses = relationship("MedicalRecord", back_populates="vet")
    inventory_actions = relationship("StockTransaction", back_populates="handled_by")
    processed_sales = relationship("MilkSale", back_populates="sold_by")

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    hire_date = Column(DateTime(timezone=True), server_default=func.now())
    is_active_employee = Column(Boolean, default=True)

    user = relationship("User", back_populates="profile")
