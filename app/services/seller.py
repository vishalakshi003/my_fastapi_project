from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.schemas.seller import SellerCreate
from app.databases.models import Seller
from app.utils import generate_access_tokens

password_context=CryptContext(schemes="bcrypt")

class SellerService:
    def __init__(self,session:AsyncSession):
        self.session=session
    async def get(self,):
        pass
    async def add(self,credentials:SellerCreate)->Seller:
        seller=Seller(
            **credentials.model_dump(exclude=["password"]),
            #hash password
            password_hash=password_context.hash(credentials.password)
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller
    
    async def token(self,email,password):
        results=await self.session.execute(select(Seller).where(Seller.email==email))
        seller= results.scalar()#fetch one
        if seller is None or not password_context.verify(password,seller.password_hash):
            raise HTTPException(status_code=404,detail='Email or Password is incorrect')
        
        token = generate_access_tokens(data={
            "user":{
                    "id":seller.id,
                    "name":seller.name,
                },
        })
        return token