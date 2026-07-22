from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.ledger import FarmerLedgerResponse
from app.services.ledger_service import get_farmer_ledger

router = APIRouter(
    prefix="/ledger",
    tags=["Ledger"]
)


@router.get("/{farmer_id}", response_model=FarmerLedgerResponse)
def farmer_ledger(
    farmer_id: int,
    from_date: date,
    to_date: date,
    db: Session = Depends(get_db)
):
    return get_farmer_ledger(
        db=db,
        farmer_id=farmer_id,
        from_date=from_date,
        to_date=to_date
    )