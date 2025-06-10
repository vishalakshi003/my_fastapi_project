from typing_extensions import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.databases.redis import add_jti_to_blacklist

from ..schemas.seller import SellerCreate, SellerResponse
from ..dependencies import SellerServiceDep, get_access_tokens
router = APIRouter(prefix="/seller", tags=["seller"])


@router.post(
    "/signup",
    response_model=SellerResponse,
    response_description="success",
    status_code=201,
)
async def register_seller(self, data: SellerCreate, service: SellerServiceDep):
    seller = await service.add(data)
    return seller


@router.post("/login",response_description="Login Successfully")
async def login_api(
    request_form: Annotated[OAuth2PasswordRequestForm,Depends()],
    service:SellerServiceDep,
):
    token= await service.token(request_form.username,request_form.password)
    return {
        "access_token":token,
        "type":"jwt"
    }
@router.get('/logout')
async def logout_seller(token:Annotated[dict,Depends(get_access_tokens)]):
    await add_jti_to_blacklist(token["jti"])
    return {
        "details":"Successfully logged out"
    }