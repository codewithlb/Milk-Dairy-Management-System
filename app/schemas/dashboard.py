from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_farmers: int
    total_milk_collected: float
    today_milk_collection: float
    total_payments: float
    pending_payments: int
    approved_payments: int
    paid_payments: int