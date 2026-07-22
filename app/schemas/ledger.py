from datetime import date
from pydantic import BaseModel


class PaymentItem(BaseModel):
    id: int
    total_amount: float
    status: str

    class Config:
        from_attributes = True


class FarmerLedgerResponse(BaseModel):
    farmer_id: int
    from_date: date
    to_date: date
    total_collections: int
    total_liters: float
    total_amount: float
    payments: list[PaymentItem]