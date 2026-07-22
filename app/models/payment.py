from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from app.database.database import Base
from datetime import date

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"))

    from_date = Column(Date)
    to_date = Column(Date)

    total_liters = Column(Float)
    total_amount = Column(Float)

    status = Column(String, default="Pending")

    payment_date = Column(Date, nullable=True)
    payment_method = Column(String, nullable=True)