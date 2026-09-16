from pydantic import BaseModel, ConfigDict, condecimal
from typing import Optional
from datetime import datetime
from models.sales import PaymentEnum

class CustomerCreate(BaseModel):
    name: str
    phone: str
    address: Optional[str] = None
    is_active: bool = True

class CustomerResponse(CustomerCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MilkSaleCreate(BaseModel):
    customer_id: int
    quantity_liters: condecimal(gt=0, max_digits=8, decimal_places=2)
    price_per_liter: condecimal(gt=0, max_digits=6, decimal_places=2)
    payment_status: PaymentEnum = PaymentEnum.PENDING
    notes: Optional[str] = None

class MilkSaleResponse(MilkSaleCreate):
    id: int
    total_amount: float
    sold_by_id: int
    date: datetime
    model_config = ConfigDict(from_attributes=True)