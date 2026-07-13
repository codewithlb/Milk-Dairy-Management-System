from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sqlalchemy import func

from app.database.database import get_db
from datetime import date
from app.models.milk_collection import MilkCollection
from app.schemas.milk_collection import (
    MilkCollectionCreate,
    MilkCollectionUpdate
)

router = APIRouter(
    prefix="/milk-collections",
    tags=["Milk Collection"]
)


@router.post("/")
def add_milk_collection(
    milk: MilkCollectionCreate,
    db: Session = Depends(get_db)
):
    # Check for duplicate entry
    print("Farmer ID:", milk.farmer_id)
    print("Date:", milk.collection_date)
    print("Shift:", milk.shift)
    existing_entry = db.query(MilkCollection).filter(
        MilkCollection.farmer_id == milk.farmer_id,
        MilkCollection.collection_date == milk.collection_date,
        MilkCollection.shift == milk.shift
    ).first()
    print("Existing Entry:", existing_entry)

    if existing_entry:
     raise HTTPException(
        status_code=400,
        detail="Milk entry already exists for this farmer, date and shift."
    )

    # Calculate amount
    amount = milk.quantity * milk.rate

    # Create new entry
    new_entry = MilkCollection(
        farmer_id=milk.farmer_id,
        collection_date=milk.collection_date,
        shift=milk.shift,
        quantity=milk.quantity,
        fat=milk.fat,
        snf=milk.snf,
        rate=milk.rate,
        amount=amount
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry

@router.get("/")
def get_milk_collections(db: Session = Depends(get_db)):
    return db.query(MilkCollection).all()

@router.put("/{milk_id}")
def update_milk_collection(
    milk_id: int,
    milk: MilkCollectionUpdate,
    db: Session = Depends(get_db)
):
    existing = db.query(MilkCollection).filter(
        MilkCollection.id == milk_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
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

@router.delete("/{milk_id}")
def delete_milk_collection(
    milk_id: int,
    db: Session = Depends(get_db)
):
    milk = db.query(MilkCollection).filter(
        MilkCollection.id == milk_id
    ).first()

    if not milk:
        raise HTTPException(
            status_code=404,
            detail="Milk collection not found."
        )

    db.delete(milk)
    db.commit()

    return {
        "message": "Milk collection deleted successfully."
    }

@router.get("/farmer/{farmer_id}")
def get_milk_by_farmer(
    farmer_id: int,
    db: Session = Depends(get_db)
):
    collections = db.query(MilkCollection).filter(
        MilkCollection.farmer_id == farmer_id
    ).all()

    if not collections:
        raise HTTPException(
            status_code=404,
            detail="No milk collections found for this farmer."
        )

    return collections

@router.get("/date/{collection_date}")
def get_milk_by_date(
    collection_date: date,
    db: Session = Depends(get_db)
):
    collections = db.query(MilkCollection).filter(
        MilkCollection.collection_date == collection_date
    ).all()

    if not collections:
        raise HTTPException(
            status_code=404,
            detail="No milk collections found for this date."
        )

    return collections

@router.get("/summary/{collection_date}")
def daily_summary(
    collection_date: date,
    db: Session = Depends(get_db)
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