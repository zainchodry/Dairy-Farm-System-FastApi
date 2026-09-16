from pydantic import BaseModel, ConfigDict, condecimal
from datetime import date, datetime
from typing import Optional
from models.livestock import GenderEnum, HealthEnum, ShiftEnum

class CattleCreate(BaseModel):
    tag_number: str
    breed: str
    gender: GenderEnum = GenderEnum.COW
    date_of_birth: date
    health_status: HealthEnum = HealthEnum.HEALTHY
    is_milking: bool = False

class CattleResponse(CattleCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MilkYieldCreate(BaseModel):
    cattle_id: int
    date: date
    shift: ShiftEnum
    volume_in_liters: condecimal(gt=0, max_digits=5, decimal_places=2)

class MilkYieldResponse(MilkYieldCreate):
    id: int
    milked_by_id: int
    model_config = ConfigDict(from_attributes=True)

class MedicalRecordCreate(BaseModel):
    cattle_id: int
    diagnosis: str
    treatment: str
    next_checkup: Optional[date] = None
    cost: condecimal(ge=0, max_digits=8, decimal_places=2) = 0.00

class MedicalRecordResponse(MedicalRecordCreate):
    id: int
    vet_id: int
    date_examined: datetime
    model_config = ConfigDict(from_attributes=True)