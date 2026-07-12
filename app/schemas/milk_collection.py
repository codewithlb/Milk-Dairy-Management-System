from pydantic import BaseModel
from datetime import date


class MilkCollectionCreate(BaseModel):
    farmer_id: int
    collection_date: date
    shift: str
    quantity: float
    fat: float
    snf: float
    rate: float


class MilkCollectionResponse(BaseModel):
    id: int
    farmer_id: int
    collection_date: date
    shift: str
    quantity: float
    fat: float
    snf: float
    rate: float
    amount: float

    class Config:
        from_attributes = True