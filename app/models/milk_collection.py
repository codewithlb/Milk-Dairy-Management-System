from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Date,
    ForeignKey,
    UniqueConstraint
)

from app.database.database import Base


class MilkCollection(Base):
    __tablename__ = "milk_collection"

    __table_args__ = (
        UniqueConstraint(
            "farmer_id",
            "collection_date",
            "shift",
            name="uq_farmer_date_shift"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"))
    collection_date = Column(Date)
    shift = Column(String)
    quantity = Column(Float)
    fat = Column(Float)
    snf = Column(Float)
    rate = Column(Float)
    amount = Column(Float)