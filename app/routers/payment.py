from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.payment import PaymentCreate
from app.services.payment_service import calculate_payment

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/calculate")
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):
    return calculate_payment(
        db=db,
        farmer_id=payment.farmer_id,
        from_date=payment.from_date,
        to_date=payment.to_date
    )