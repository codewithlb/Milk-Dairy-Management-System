from sqlalchemy import Column, Integer, String
from app.database.database import Base

class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    mobile = Column(String, unique=True)
    address = Column(String)