from datetime import date

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_admin

from app.models.payment import Payment

from app.schemas.report import (
    DailyReportResponse,
    FarmerReportResponse,
)

from app.services.report_service import (
    daily_collection_report,
    farmer_collection_report,
)

from app.services.excel_service import export_payments_excel


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


# ============================================================
# DAILY MILK REPORT
# ============================================================

@router.get(
    "/daily",
    response_model=DailyReportResponse
)
def get_daily_report(
    report_date: date,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return daily_collection_report(
        db=db,
        report_date=report_date
    )


# ============================================================
# FARMER-WISE MILK REPORT
# ============================================================

@router.get(
    "/farmer/{farmer_id}",
    response_model=FarmerReportResponse
)
def get_farmer_report(
    farmer_id: int,
    from_date: date,
    to_date: date,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return farmer_collection_report(
        db=db,
        farmer_id=farmer_id,
        from_date=from_date,
        to_date=to_date
    )


# ============================================================
# PAYMENT EXCEL EXPORT
# ============================================================

@router.get("/export/payments")
def export_payment_report(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    payments = db.query(Payment).all()

    filename = "payments_report.xlsx"

    export_payments_excel(
        payments,
        filename
    )

    return FileResponse(
        filename,
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        filename="payments_report.xlsx"
    )