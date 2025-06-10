"""it's service file, to create a service for shipments"""

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.shipment import ShipmentCreate, ShipmentResponse, ShipmentUpdate
from app.databases.models import Seller, ShipmentStatus, Shipments
# from app.databases.session import SessionDep


class ShipmentService:
    def __init__(self,session:AsyncSession):
        self.session=session

    async def get(self,id:int)->ShipmentResponse:
        return await self.session.get(Shipments,id)
    
    async def add(self,shipment_create:ShipmentCreate,seller:Seller)->Shipments:
        new_data=Shipments(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            created_at=datetime.now(),
            seller_id=seller.id,
        )
        self. session.add(new_data)
        await self.session.commit()
        await self.session.refresh(new_data)
        return new_data
    
    async def update(self,id:int,shipment_update:ShipmentUpdate)->Shipments:
        data=await self.get(id)#take in get
        data.sqlmodel_update(shipment_update)
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data
    
    async def delete(self,id:int)->None:
        data=await self.get(id)
        data.is_active=False
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return id