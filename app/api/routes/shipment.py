"""this is api endpoint file"""

from fastapi import APIRouter
from fastapi import HTTPException, status
from app.api.dependencies import SellerDeps, ServiceDep
from app.databases.models import Shipments
from app.api.schemas.shipment import ShipmentCreate, ShipmentResponse, ShipmentUpdate


router = APIRouter(tags=["Shipments"])


@router.get("/shipments", status_code=200, response_description="Success")
async def get_details(id: int,seller:SellerDeps,service: ServiceDep):
    shipment = await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found"
        )
    return shipment


@router.post("/shipments", status_code=201)
async def create_data(#shift+alt+f
    seller:SellerDeps,
    req_data: ShipmentCreate,
    service: ServiceDep,
) -> Shipments:
    return await service.add(req_data , seller)


# @router.put("/shipments",response_model=ShipmentResponse,status_code=200)
# def update_data(id:int,up_data:UpdateAll,session:SessionDep):
#     data=session.get(Shipments,id)
#     data.sqlmodel_update(up_data)
#     session.add(data)
#     session.commit()
#     session.refresh(data)
#     return data


@router.patch("/shipments", response_model=ShipmentResponse, status_code=200)
async def update_fields(id: int, upd_data: ShipmentUpdate, service: ServiceDep):
    update = upd_data.model_dump(exclude_none=True)
    if not update:
        raise HTTPException(status_code=400, detail="no data provided")
    data = await service.update(id, update)
    return data


@router.delete("/shipments", status_code=200)
async def delete_data(id: int, service: ServiceDep):
    await service.delete(id)
    return {"details": f"user {id} delete successfully!"}
