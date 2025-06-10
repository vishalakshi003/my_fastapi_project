"""it's a starting point of fastapi"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from rich import panel, print  # for display different style in print message
from scalar_fastapi import get_scalar_api_reference
from app.databases.session import create_db_tables
from app.api.route import master_router

#lifespan of server
"""it provides a clean and async-safe way to manage startup and shutdown logic in one place."""
@asynccontextmanager
async def lifesapan_handler(app:FastAPI):
    await create_db_tables()
    print(panel.Panel("server start........",border_style="green"))
    yield
    print(panel.Panel("server stop........",border_style="red"))

app=FastAPI(lifespan=lifesapan_handler)
app.include_router(master_router)


"""used to connect scaler.docs"""
@app.get('/scalar',include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title='Scalar API',
    ) 