from fastapi import FastAPI
from app.models.payment import Payment

from app.database.database import Base, engine
from app.models.farmer import Farmer
from app.models.milk_collection import MilkCollection
from app.routers import payment
from app.routers import farmer
from app.routers import milk_collection
from app.routers import dashboard
from app.routers import report
from app.routers import ledger

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Milk Dairy Management API")

# Register Routers
app.include_router(farmer.router)
app.include_router(milk_collection.router)
app.include_router(payment.router)
app.include_router(dashboard.router)
app.include_router(report.router)
app.include_router(ledger.router)


@app.get("/")
def home():
    return {
        "message": "Milk Dairy API Running 🚀"
    }