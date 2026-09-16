from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class GenderEnum(str, enum.Enum):
    BULL = "BULL"
    COW = "COW"
    CALF = "CALF"

class HealthEnum(str, enum.Enum):
    HEALTHY = "HEALTHY"
    SICK = "SICK"
    SOLD = "SOLD"
    DECEASED = "DECEASED"

class ShiftEnum(str, enum.Enum):
    MORNING = "MORNING"
    EVENING = "EVENING"

class Cattle(Base):
    __tablename__ = "cattle"
    
    id = Column(Integer, primary_key=True, index=True)
    tag_number = Column(String, unique=True, index=True)
    breed = Column(String)
    gender = Column(Enum(GenderEnum), default=GenderEnum.COW)
    date_of_birth = Column(Date)
    health_status = Column(Enum(HealthEnum), default=HealthEnum.HEALTHY)
    is_milking = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    yields = relationship("MilkYield", back_populates="cattle")
    medical_records = relationship("MedicalRecord", back_populates="cattle")

class MilkYield(Base):
    __tablename__ = "milk_yields"
    
    id = Column(Integer, primary_key=True, index=True)
    cattle_id = Column(Integer, ForeignKey("cattle.id", ondelete="CASCADE"))
    milked_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    date = Column(Date)
    shift = Column(Enum(ShiftEnum))
    volume_in_liters = Column(Numeric(5, 2))

    cattle = relationship("Cattle", back_populates="yields")
    milked_by = relationship("User", back_populates="milking_logs")

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    
    id = Column(Integer, primary_key=True, index=True)
    cattle_id = Column(Integer, ForeignKey("cattle.id", ondelete="CASCADE"))
    vet_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"))
    diagnosis = Column(String)
    treatment = Column(String)
    date_examined = Column(DateTime(timezone=True), server_default=func.now())
    next_checkup = Column(Date, nullable=True)
    cost = Column(Numeric(8, 2), default=0.00)

    cattle = relationship("Cattle", back_populates="medical_records")
    vet = relationship("User", back_populates="diagnoses")