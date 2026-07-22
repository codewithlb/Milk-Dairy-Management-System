from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.payment import Payment


from app.database.database import get_db
from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse
from app.services.payment_service import approve_payment

from app.schemas.payment import PaymentUpdate
from app.services.payment_service import mark_payment_paid,get_farmer_payments

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

@router.get("/")
def get_all_payments(db: Session = Depends(get_db)):
    from app.models.payment import Payment

    return db.query(Payment).all()





@router.patch("/{payment_id}/pay", response_model=PaymentResponse)
def pay_payment(
    payment_id: int,
    payment: PaymentUpdate,
    db: Session = Depends(get_db)
):
    return mark_payment_paid(
        db=db,
        payment_id=payment_id,
        payment_method=payment.payment_method
    )

@router.put("/{payment_id}/approve", response_model=PaymentResponse)
def approve_payment_route(
    payment_id: int,
    db: Session = Depends(get_db)
):
    return approve_payment(db, payment_id)


@router.get("/farmer/{farmer_id}", response_model=list[PaymentResponse])
def get_payment_history(
    farmer_id: int,
    db: Session = Depends(get_db)
):
    return get_farmer_payments(db, farmer_id)