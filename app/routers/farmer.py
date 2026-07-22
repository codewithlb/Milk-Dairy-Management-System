from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.farmer import Farmer
from app.schemas.farmer import FarmerCreate
from app.dependencies.auth import get_current_admin

router = APIRouter(prefix="/farmers", tags=["Farmers"])


@router.post("/")
def add_farmer(farmer: FarmerCreate, db: Session = Depends(get_db)):
    new_farmer = Farmer(
        name=farmer.name,
        mobile=farmer.mobile,
        address=farmer.address
    )

    db.add(new_farmer)
    db.commit()
    db.refresh(new_farmer)

    return new_farmer


@router.get("/")
def get_farmers(
    db: Session = Depends(get_db)
):
    return db.query(Farmer).all()