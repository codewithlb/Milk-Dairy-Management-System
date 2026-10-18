from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.farmer import Farmer
from app.models.milk_collection import MilkCollection


def create_milk_collection(
    db: Session,
    milk_data
):
    # =========================
    # CHECK FARMER EXISTS
    # =========================
    farmer = db.query(Farmer).filter(
        Farmer.id == milk_data.farmer_id
    ).first()

    if farmer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found."
        )

    # =========================
    # CHECK DUPLICATE COLLECTION
    # =========================
    existing = db.query(MilkCollection).filter(
        MilkCollection.farmer_id == milk_data.farmer_id,
        MilkCollection.collection_date == milk_data.collection_date,
        MilkCollection.shift == milk_data.shift
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Milk already collected for this farmer in this shift."
        )

    # =========================
    # CALCULATE AMOUNT
    # =========================
    amount = milk_data.quantity * milk_data.rate

    milk = MilkCollection(
        farmer_id=milk_data.farmer_id,
        collection_date=milk_data.collection_date,
        shift=milk_data.shift,
        quantity=milk_data.quantity,
        fat=milk_data.fat,
        snf=milk_data.snf,
        rate=milk_data.rate,
        amount=amount
    )

    db.add(milk)

    try:
        db.commit()
        db.refresh(milk)

        return milk

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Milk collection already exists for this farmer, date and shift."
        )