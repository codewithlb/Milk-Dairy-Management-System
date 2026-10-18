from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.farmer import Farmer
from app.models.milk_collection import MilkCollection
from app.models.payment import Payment


def calculate_payment(
    db: Session,
    farmer_id: int,
    from_date,
    to_date
):
    # --------------------------------------------------------
    # Validate date range
    # --------------------------------------------------------

    if from_date > to_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="From date cannot be after to date."
        )

    # --------------------------------------------------------
    # Check farmer
    # --------------------------------------------------------

    farmer = db.query(Farmer).filter(
        Farmer.id == farmer_id
    ).first()

    if farmer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found."
        )

    # --------------------------------------------------------
    # Check duplicate payment
    # --------------------------------------------------------

    existing_payment = db.query(Payment).filter(
        Payment.farmer_id == farmer_id,
        Payment.from_date == from_date,
        Payment.to_date == to_date
    ).first()

    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Payment has already been generated for this date range."
        )

    # --------------------------------------------------------
    # Calculate milk totals
    # --------------------------------------------------------

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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No milk collection found for the selected date range."
        )

    # --------------------------------------------------------
    # Create payment
    # --------------------------------------------------------

    payment = Payment(
        farmer_id=farmer_id,
        from_date=from_date,
        to_date=to_date,
        total_liters=total_liters,
        total_amount=total_amount,
        status="Pending"
    )

    db.add(payment)

    try:
        db.commit()
        db.refresh(payment)

        return payment

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Payment already exists for this farmer and date range."
        )


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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found."
        )

    if payment.status == "Paid":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Payment is already marked as paid."
        )

    if payment.status != "Approved":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment must be approved before marking it as paid."
        )

    payment.status = "Paid"
    payment.payment_method = payment_method
    payment.payment_date = date.today()

    try:
        db.commit()
        db.refresh(payment)

        return payment

    except Exception:
        db.rollback()
        raise


def approve_payment(
    db: Session,
    payment_id: int
):
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found."
        )

    if payment.status == "Approved":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Payment is already approved."
        )

    if payment.status == "Paid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Paid payment cannot be approved again."
        )

    payment.status = "Approved"

    try:
        db.commit()
        db.refresh(payment)

        return payment

    except Exception:
        db.rollback()
        raise


def get_farmer_payments(
    db: Session,
    farmer_id: int
):
    farmer = db.query(Farmer).filter(
        Farmer.id == farmer_id
    ).first()

    if farmer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found."
        )

    payments = (
        db.query(Payment)
        .filter(Payment.farmer_id == farmer_id)
        .order_by(Payment.from_date.desc())
        .all()
    )

    if not payments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No payments found for this farmer."
        )

    return payments