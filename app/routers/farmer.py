from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.farmer import Farmer
from app.schemas.farmer import FarmerCreate
from app.dependencies.auth import get_current_admin
from app.dependencies.roles import require_superadmin

router = APIRouter(
    prefix="/farmers",
    tags=["Farmers"]
)


@router.post("/")
def add_farmer(
    farmer: FarmerCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
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
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(Farmer).all()


@router.delete("/{farmer_id}")
def delete_farmer(
    farmer_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_superadmin)
):
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()

    if farmer is None:
        return {"message": "Farmer not found"}

    db.delete(farmer)
    db.commit()

    return {"message": "Farmer deleted successfully"}