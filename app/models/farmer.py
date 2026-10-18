from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    mobile = Column(
        String,
        unique=True
    )

    address = Column(
        String
    )

    milk_collections = relationship(
        "MilkCollection",
        back_populates="farmer",
        cascade="all, delete"
    )

    payments = relationship(
        "Payment",
        back_populates="farmer",
        cascade="all, delete"
    )