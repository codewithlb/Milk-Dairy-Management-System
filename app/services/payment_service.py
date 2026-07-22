from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.milk_collection import MilkCollection
from app.models.payment import Payment


def calculate_payment(db: Session, farmer_id: int, from_date, to_date):

    # Check if payment already exists
    existing_payment = db.query(Payment).filter(
        Payment.farmer_id == farmer_id,
        Payment.from_date == from_date,
        Payment.to_date == to_date
    ).first()

    if existing_payment:
        raise HTTPException(
            status_code=400,
            detail="Payment has already been generated for this date range."
        )

    # Calculate totals
    result = db.query(
        func.sum(MilkCollection.quantity),
        func.sum(MilkCollection.amount)
    ).filter(
        MilkCollection.farmer_id == farmer_id,
        MilkCollection.collection_date >= from_date,
        MilkCollection.collection_date <= to_date
    ).first()

    total_liters = result[0] or 0
    total_amount = result[1] or 0

    if total_liters == 0:
        raise HTTPException(
            status_code=404,
            detail="No milk collection found for the selected date range."
        )

    payment = Payment(
        farmer_id=farmer_id,
        from_date=from_date,
        to_date=to_date,
        total_liters=total_liters,
        total_amount=total_amount,
        status="Pending"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment

from datetime import date


def mark_payment_paid(
    db: Session,
    payment_id: int,
    payment_method: str
):
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found."
        )

    if payment.status == "Paid":
        raise HTTPException(
            status_code=400,
            detail="Payment is already marked as paid."
        )

    payment.status = "Paid"
    payment.payment_method = payment_method
    payment.payment_date = date.today()

    db.commit()
    db.refresh(payment)

    return payment
def approve_payment(db: Session, payment_id: int):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found.")

    if payment.status == "Approved":
        raise HTTPException(
            status_code=400,
            detail="Payment already approved."
        )

    payment.status = "Approved"
    db.commit()
    db.refresh(payment)

    return payment