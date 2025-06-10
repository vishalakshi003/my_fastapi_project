"""this file is to create a service b/w session and ShipmentService--> to inject"""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException,status
from typing_extensions import Annotated
from app.databases.models import Seller
from app.databases.redis import check_is_jti
from app.databases.session import get_session
from app.services.shipment import ShipmentService
from app.utils import decode_access_tokens
from ..services.seller import SellerService
from ..core.security import oauth2_scheme
#session sependecy annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]

# this fn not required async
#it is used for service
def get_shipment_service(session:SessionDep):
    return ShipmentService(session)
def get_seller_service(session:SessionDep):
    return SellerService(session)

#Access token data
async def get_access_tokens(token:Annotated[str,Depends(oauth2_scheme)])->dict:
    data=decode_access_tokens(token=token)
    
    if data is None or await check_is_jti(data["jti"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or Expired access tokens")
    return data
async def get_current_seller(token_data:Annotated[dict,Depends(get_access_tokens)],session:SessionDep):
    seller=await session.get(Seller,token_data["user"]["id"])
    return seller

#shipment service dep annotation
ServiceDep=Annotated[ShipmentService,Depends(get_shipment_service)]
#seller service dep annotation
SellerServiceDep=Annotated[SellerService,Depends(get_seller_service)]

#Seller Deps
SellerDeps=Annotated[Seller,Depends(get_current_seller)]