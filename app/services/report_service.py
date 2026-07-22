from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.milk_collection import MilkCollection


def daily_collection_report(db: Session, report_date: date):
    collections = (
        db.query(MilkCollection)
        .filter(MilkCollection.collection_date == report_date)
        .all()
    )

    total_liters = (
        db.query(func.sum(MilkCollection.quantity))
        .filter(MilkCollection.collection_date == report_date)
        .scalar() or 0
    )

    total_amount = (
        db.query(func.sum(MilkCollection.amount))
        .filter(MilkCollection.collection_date == report_date)
        .scalar() or 0
    )

    return {
        "date": report_date,
        "total_liters": total_liters,
        "total_amount": total_amount,
        "collections": collections
    }