from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_admin
from app.models.farmer import Farmer
from app.models.milk_collection import MilkCollection
from app.schemas.milk_collection import (
    MilkCollectionCreate,
    MilkCollectionUpdate
)
from app.services.milk_collection_service import create_milk_collection


router = APIRouter(
    prefix="/milk-collections",
    tags=["Milk Collection"]
)


# =========================
# ADD MILK COLLECTION
# =========================
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def add_milk_collection(
    milk: MilkCollectionCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return create_milk_collection(db, milk)


# =========================
# GET ALL MILK COLLECTIONS
# =========================
@router.get("/")
def get_milk_collections(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    collections = (
        db.query(MilkCollection, Farmer)
        .join(
            Farmer,
            MilkCollection.farmer_id == Farmer.id
        )
        .all()
    )

    result = []

    for milk, farmer in collections:
        result.append({
            "id": milk.id,
            "farmer_id": milk.farmer_id,
            "farmer_name": farmer.name,
            "collection_date": milk.collection_date,
            "shift": milk.shift,
            "quantity": milk.quantity,
            "fat": milk.fat,
            "snf": milk.snf,
            "rate": milk.rate,
            "amount": milk.amount
        })

    return result


# =========================
# UPDATE MILK COLLECTION
# =========================
@router.put("/{milk_id}")
def update_milk_collection(
    milk_id: int,
    milk: MilkCollectionUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    existing = db.query(MilkCollection).filter(
        MilkCollection.id == milk_id
    ).first()

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Milk collection not found."
        )

    existing.quantity = milk.quantity
    existing.fat = milk.fat
    existing.snf = milk.snf
    existing.rate = milk.rate
    existing.amount = milk.quantity * milk.rate

    db.commit()
    db.refresh(existing)

    return existing


# =========================
# DELETE MILK COLLECTION
# =========================
@router.delete("/{milk_id}")
def delete_milk_collection(
    milk_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    milk = db.query(MilkCollection).filter(
        MilkCollection.id == milk_id
    ).first()

    if milk is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Milk collection not found."
        )

    db.delete(milk)
    db.commit()

    return {
        "message": "Milk collection deleted successfully."
    }


# =========================
# GET MILK BY FARMER
# =========================
@router.get("/farmer/{farmer_id}")
def get_milk_by_farmer(
    farmer_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    collections = db.query(MilkCollection).filter(
        MilkCollection.farmer_id == farmer_id
    ).all()

    if not collections:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No milk collections found for this farmer."
        )

    return collections


# =========================
# GET MILK BY DATE
# =========================
@router.get("/date/{collection_date}")
def get_milk_by_date(
    collection_date: date,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    collections = db.query(MilkCollection).filter(
        MilkCollection.collection_date == collection_date
    ).all()

    if not collections:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No milk collections found for this date."
        )

    return collections


# =========================
# DAILY SUMMARY
# =========================
@router.get("/summary/{collection_date}")
def daily_summary(
    collection_date: date,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    result = db.query(
        func.count(MilkCollection.id),
        func.sum(MilkCollection.quantity),
        func.sum(MilkCollection.amount)
    ).filter(
        MilkCollection.collection_date == collection_date
    ).first()

    return {
        "date": collection_date,
        "total_collections": result[0] or 0,
        "total_liters": result[1] or 0,
        "total_amount": result[2] or 0
    }