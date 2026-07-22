from pydantic import BaseModel
from datetime import date

class PaymentUpdate(BaseModel):
    payment_method: str

class PaymentCreate(BaseModel):
    farmer_id: int
    from_date: date
    to_date: date


class PaymentResponse(BaseModel):
    id: int
    farmer_id: int
    from_date: date
    to_date: date
    total_liters: float
    total_amount: float
    status: str

    class Config:
        from_attributes = True

 