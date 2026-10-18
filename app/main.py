from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.payment import Payment
from app.models.admin import Admin

from app.database.database import Base, engine
from app.models.farmer import Farmer
from app.models.milk_collection import MilkCollection

from app.routers import payment
from app.routers import farmer
from app.routers import milk_collection
from app.routers import dashboard
from app.routers import report
from app.routers import ledger
from app.routers import auth


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Milk Dairy Management API")


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register Routers
app.include_router(farmer.router)
app.include_router(milk_collection.router)
app.include_router(payment.router)
app.include_router(dashboard.router)
app.include_router(report.router)
app.include_router(ledger.router)
app.include_router(auth.router)


@app.get("/")
def home():
    return {
        "message": "Milk Dairy API Running 🚀"
    }