from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.farmer import Farmer
from app.models.milk_collection import MilkCollection


def daily_collection_report(
    db: Session,
    report_date: date
):
    collections = (
        db.query(MilkCollection)
        .filter(
            MilkCollection.collection_date == report_date
        )
        .all()
    )

    if not collections:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No milk collection found for this date."
        )

    total_liters = (
        db.query(
            func.sum(MilkCollection.quantity)
        )
        .filter(
            MilkCollection.collection_date == report_date
        )
        .scalar()
        or 0
    )

    total_amount = (
        db.query(
            func.sum(MilkCollection.amount)
        )
        .filter(
            MilkCollection.collection_date == report_date
        )
        .scalar()
        or 0
    )

    return {
        "date": report_date,
        "total_liters": total_liters,
        "total_amount": total_amount,
        "collections": collections
    }


def farmer_collection_report(
    db: Session,
    farmer_id: int,
    from_date: date,
    to_date: date
):
    if from_date > to_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="From date cannot be after to date."
        )

    farmer = (
        db.query(Farmer)
        .filter(Farmer.id == farmer_id)
        .first()
    )

    if farmer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found."
        )

    collections = (
        db.query(MilkCollection)
        .filter(
            MilkCollection.farmer_id == farmer_id,
            MilkCollection.collection_date >= from_date,
            MilkCollection.collection_date <= to_date
        )
        .order_by(
            MilkCollection.collection_date
        )
        .all()
    )

    if not collections:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No milk collection found for this farmer and date range."
        )

    total_liters = sum(
        collection.quantity or 0
        for collection in collections
    )

    total_amount = sum(
        collection.amount or 0
        for collection in collections
    )

    return {
        "farmer_id": farmer.id,
        "farmer_name": farmer.name,
        "from_date": from_date,
        "to_date": to_date,
        "total_liters": total_liters,
        "total_amount": total_amount,
        "collections": collections
    }