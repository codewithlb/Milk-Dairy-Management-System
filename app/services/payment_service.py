from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.milk_collection import MilkCollection
from app.models.payment import Payment


def calculate_payment(db: Session, farmer_id: int, from_date, to_date):

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