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


class FarmerReportResponse(BaseModel):
    farmer_id: int
    farmer_name: str
    from_date: date
    to_date: date
    total_liters: float
    total_amount: float
    collections: list[MilkCollectionItem]