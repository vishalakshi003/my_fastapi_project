"""create models"""

from datetime import datetime
from enum import Enum
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from typing import List

class ShipmentStatus(str, Enum):
    placed = "placed"
    intransit = "intransit"
    out_of_delivery = "out_of_delivery"


class Shipments(SQLModel, table=True):
    __tablename__ = "shipments"

    id: int = Field(default=None, primary_key=True)
    content: str = Field(le=30)
    weight: float = Field(le=25)
    destination: str
    status: ShipmentStatus
    created_at: datetime
    is_active: bool = Field(default=True)

    seller_id: int = Field(foreign_key="seller.id")  # tablename and id field
    # to access the seller details in shipment-> use relationship
    """if we change any thing in shipment models it will affect the seller relationship--> so we use back_populates--> it use to modified the changes in it"""
    seller: "Seller" = Relationship(
        back_populates="shipment",
        sa_relationship_kwargs={"lazy": "selectin"},#it will use access all the field in shipment models
    )  # name is same to relationship in seller


class Seller(SQLModel, table=True):
    __tablename__ = "seller"
    id: int = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password_hash: str
    # to access the shipment details in seller
    """if we change any thing in seller models it will affect the shipment relationship--> so we use back_populates--> it use to modified the changes in it"""

    shipment: List["Shipments"] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"},#it will use access all the field in seller models
    )
