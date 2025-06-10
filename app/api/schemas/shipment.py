"""schema file for shipments models"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel,Field
from app.databases.models import Seller, ShipmentStatus

class ShipmentBase(BaseModel):
    content:str
    weight:float
    destination:str

class ShipmentCreate(ShipmentBase):
    pass
class ShipmentResponse(ShipmentBase):
    seller:Seller
    status:ShipmentStatus
    created_at:datetime

class UpdateAll(ShipmentBase):
    status:str
class ShipmentUpdate(BaseModel):
    status: Optional[ShipmentStatus] = Field(default=None)
    destination: Optional[str] = Field(default=None)

    
