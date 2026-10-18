from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.farmer import Farmer
from app.schemas.farmer import FarmerCreate, FarmerUpdate
from app.dependencies.auth import get_current_admin
from app.dependencies.roles import require_superadmin


router = APIRouter(
    prefix="/farmers",
    tags=["Farmers"]
)


# =========================
# ADD FARMER
# =========================
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_farmer(
    farmer: FarmerCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    # Check duplicate mobile
    existing_farmer = db.query(Farmer).filter(
        Farmer.mobile == farmer.mobile
    ).first()

    if existing_farmer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Farmer with this mobile number already exists"
        )

    new_farmer = Farmer(
        name=farmer.name,
        mobile=farmer.mobile,
        address=farmer.address
    )

    db.add(new_farmer)
    db.commit()
    db.refresh(new_farmer)

    return new_farmer


# =========================
# GET ALL FARMERS
# =========================
@router.get("/")
def get_farmers(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(Farmer).all()


# =========================
# GET FARMER BY ID
# =========================
@router.get("/{farmer_id}")
def get_farmer(
    farmer_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    farmer = db.query(Farmer).filter(
        Farmer.id == farmer_id
    ).first()

    if farmer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found"
        )

    return farmer


# =========================
# UPDATE FARMER
# =========================
@router.put("/{farmer_id}")
def update_farmer(
    farmer_id: int,
    farmer: FarmerUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_farmer = db.query(Farmer).filter(
        Farmer.id == farmer_id
    ).first()

    if db_farmer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found"
        )

    # Check if mobile belongs to another farmer
    existing_farmer = db.query(Farmer).filter(
        Farmer.mobile == farmer.mobile,
        Farmer.id != farmer_id
    ).first()

    if existing_farmer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Another farmer already uses this mobile number"
        )

    db_farmer.name = farmer.name
    db_farmer.mobile = farmer.mobile
    db_farmer.address = farmer.address

    db.commit()
    db.refresh(db_farmer)

    return db_farmer


# =========================
# DELETE FARMER
# =========================
@router.delete("/{farmer_id}")
def delete_farmer(
    farmer_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_superadmin)
):
    farmer = db.query(Farmer).filter(
        Farmer.id == farmer_id
    ).first()

    if farmer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found"
        )

    db.delete(farmer)
    db.commit()

    return {
        "message": "Farmer deleted successfully"
    }