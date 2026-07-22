from datetime import date

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.farmer import Farmer
from app.models.milk_collection import MilkCollection
from app.models.payment import Payment


def get_farmer_ledger(
    db: Session,
    farmer_id: int,
    from_date: date,
    to_date: date
):
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()

    if farmer is None:
        raise HTTPException(
            status_code=404,
            detail="Farmer not found."
        )

    collections = db.query(MilkCollection).filter(
        MilkCollection.farmer_id == farmer_id,
        MilkCollection.collection_date >= from_date,
        MilkCollection.collection_date <= to_date
    )

    total_collections = collections.count()

    total_liters = db.query(
        func.sum(MilkCollection.quantity)
    ).filter(
        MilkCollection.farmer_id == farmer_id,
        MilkCollection.collection_date >= from_date,
        MilkCollection.collection_date <= to_date
    ).scalar() or 0

    total_amount = db.query(
        func.sum(MilkCollection.amount)
    ).filter(
        MilkCollection.farmer_id == farmer_id,
        MilkCollection.collection_date >= from_date,
        MilkCollection.collection_date <= to_date
    ).scalar() or 0

    payments = db.query(Payment).filter(
        Payment.farmer_id == farmer_id,
        Payment.from_date >= from_date,
        Payment.to_date <= to_date
    ).all()

    return {
        "farmer_id": farmer_id,
        "from_date": from_date,
        "to_date": to_date,
        "total_collections": total_collections,
        "total_liters": total_liters,
        "total_amount": total_amount,
        "payments": payments
    }