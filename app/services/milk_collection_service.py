
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.models.milk_collection import MilkCollection


def create_milk_collection(db, milk_data):

    # Check duplicate entry
    existing = db.query(MilkCollection).filter(
        MilkCollection.farmer_id == milk_data.farmer_id,
        MilkCollection.collection_date == milk_data.collection_date,
        MilkCollection.shift == milk_data.shift
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Milk already collected for this farmer in this shift."
        )

    # Calculate amount
    amount = milk_data.quantity * milk_data.rate

    milk = MilkCollection(
        farmer_id=milk_data.farmer_id,
        collection_date=milk_data.collection_date,
        shift=milk_data.shift,
        quantity=milk_data.quantity,
        fat=milk_data.fat,
        snf=milk_data.snf,
        rate=milk_data.rate,
        amount=amount,
    )

    db.add(milk)

    try:
        db.commit()
        db.refresh(milk)
        return milk

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Milk already collected for this farmer in this shift."
        )