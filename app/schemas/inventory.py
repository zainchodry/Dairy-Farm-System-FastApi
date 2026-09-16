from pydantic import BaseModel, ConfigDict, condecimal
from typing import Optional
from datetime import datetime
from models.inventory import TxTypeEnum

class ItemCreate(BaseModel):
    name: str
    item_type: str
    unit_of_measure: str
    reorder_level: condecimal(ge=0, max_digits=10, decimal_places=2)

class ItemResponse(ItemCreate):
    id: int
    quantity_in_stock: float
    model_config = ConfigDict(from_attributes=True)

class StockTxCreate(BaseModel):
    item_id: int
    transaction_type: TxTypeEnum
    quantity: condecimal(gt=0, max_digits=10, decimal_places=2)
    notes: Optional[str] = None

class StockTxResponse(StockTxCreate):
    id: int
    transaction_date: datetime
    handled_by_id: int
    model_config = ConfigDict(from_attributes=True)