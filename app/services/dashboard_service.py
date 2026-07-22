from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.farmer import Farmer
from app.models.milk_collection import MilkCollection
from app.models.payment import Payment


def get_dashboard(db: Session):
    total_farmers = db.query(Farmer).count()

    total_milk = (
        db.query(func.sum(MilkCollection.quantity)).scalar() or 0
    )

    today_milk = (
        db.query(func.sum(MilkCollection.quantity))
        .filter(MilkCollection.collection_date == date.today())
        .scalar() or 0
    )

    total_payments = (
        db.query(func.sum(Payment.total_amount)).scalar() or 0
    )

    pending = (
        db.query(Payment)
        .filter(Payment.status == "Pending")
        .count()
    )

    approved = (
        db.query(Payment)
        .filter(Payment.status == "Approved")
        .count()
    )

    paid = (
        db.query(Payment)
        .filter(Payment.status == "Paid")
        .count()
    )

    return {
        "total_farmers": total_farmers,
        "total_milk_collected": total_milk,
        "today_milk_collection": today_milk,
        "total_payments": total_payments,
        "pending_payments": pending,
        "approved_payments": approved,
        "paid_payments": paid,
    }