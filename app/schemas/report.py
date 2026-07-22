from datetime import date
from pydantic import BaseModel


class MilkCollectionItem(BaseModel):
    id: int
    farmer_id: int
    quantity: float
    amount: float
    collection_date: date

    class Config:
        from_attributes = True


class DailyReportResponse(BaseModel):
    date: date
    total_liters: float
    total_amount: float
    collections: list[MilkCollectionItem]