from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_admin

from app.models.payment import Payment
from app.models.farmer import Farmer
from app.models.milk_collection import MilkCollection

from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse,
)

from app.services.payment_service import (
    calculate_payment,
    approve_payment,
    mark_payment_paid,
    get_farmer_payments,
)

from app.services.pdf_service import generate_payment_receipt


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


# ============================================================
# GENERATE PAYMENT
# ============================================================

@router.post(
    "/calculate",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return calculate_payment(
        db=db,
        farmer_id=payment.farmer_id,
        from_date=payment.from_date,
        to_date=payment.to_date
    )


# ============================================================
# GET ALL PAYMENTS
# ============================================================

@router.get(
    "/",
    response_model=list[PaymentResponse]
)
def get_all_payments(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(Payment).all()


# ============================================================
# MARK PAYMENT AS PAID
# ============================================================

@router.patch(
    "/{payment_id}/pay",
    response_model=PaymentResponse
)
def pay_payment(
    payment_id: int,
    payment: PaymentUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return mark_payment_paid(
        db=db,
        payment_id=payment_id,
        payment_method=payment.payment_method
    )


# ============================================================
# APPROVE PAYMENT
# ============================================================

@router.put(
    "/{payment_id}/approve",
    response_model=PaymentResponse
)
def approve_payment_route(
    payment_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return approve_payment(
        db=db,
        payment_id=payment_id
    )


# ============================================================
# FARMER PAYMENT HISTORY
# ============================================================

@router.get(
    "/farmer/{farmer_id}",
    response_model=list[PaymentResponse]
)
def get_payment_history(
    farmer_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return get_farmer_payments(
        db=db,
        farmer_id=farmer_id
    )


# ============================================================
# DOWNLOAD PAYMENT RECEIPT
# ============================================================

@router.get("/{payment_id}/receipt")
def download_receipt(
    payment_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    # --------------------------------------------------------
    # Find payment
    # --------------------------------------------------------

    payment = (
        db.query(Payment)
        .filter(Payment.id == payment_id)
        .first()
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found."
        )

    # --------------------------------------------------------
    # Find farmer
    # --------------------------------------------------------

    farmer = (
        db.query(Farmer)
        .filter(Farmer.id == payment.farmer_id)
        .first()
    )

    if farmer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found."
        )

    # --------------------------------------------------------
    # Get milk collections
    # --------------------------------------------------------

    milk_collections = (
        db.query(MilkCollection)
        .filter(
            MilkCollection.farmer_id == payment.farmer_id,
            MilkCollection.collection_date >= payment.from_date,
            MilkCollection.collection_date <= payment.to_date,
        )
        .order_by(
            MilkCollection.collection_date,
            MilkCollection.shift,
        )
        .all()
    )

    # --------------------------------------------------------
    # Generate PDF
    # --------------------------------------------------------

    filename = f"receipt_{payment.id}.pdf"

    generate_payment_receipt(
        payment=payment,
        farmer=farmer,
        milk_collections=milk_collections,
        filename=filename,
    )

    # --------------------------------------------------------
    # Return PDF
    # --------------------------------------------------------

    return FileResponse(
        path=filename,
        filename=filename,
        media_type="application/pdf"
    )