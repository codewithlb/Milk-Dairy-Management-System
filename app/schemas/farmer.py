from pydantic import BaseModel

class FarmerCreate(BaseModel):
    name: str
    mobile: str
    address: str

class FarmerResponse(BaseModel):
    id: int
    name: str
    mobile: str
    address: str

    class Config:
        from_attributes = True