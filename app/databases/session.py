"""this is the file to create a database connection with session, 
in fastapi we need to inject data for every request """

from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from app.config import db_settings

#create engine
engine=create_async_engine(
    url=db_settings.POSTGRES_URL,
    echo=True #print data in terminal
)

"""used to create_table"""
async def create_db_tables():
    async with engine.begin() as connection:
        from app.databases.models import Shipments,Seller
        await connection.run_sync(SQLModel.metadata.create_all)


"""used to create session in async"""
async def get_session():#database setup
    async_session= sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)
    
    async with async_session() as session:
        yield session
# #session sependecy annotation
# SessionDep = Annotated[AsyncSession, Depends(get_session)]