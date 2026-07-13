from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey
from app.database.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"))

    from_date = Column(Date)
    to_date = Column(Date)

    total_liters = Column(Float)
    total_amount = Column(Float)

    status = Column(String, default="Pending")