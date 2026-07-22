from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.report import DailyReportResponse
from app.services.report_service import daily_collection_report

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/daily", response_model=DailyReportResponse)
def get_daily_report(
    report_date: date,
    db: Session = Depends(get_db)
):
    return daily_collection_report(db, report_date)