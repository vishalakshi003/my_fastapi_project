from redis.asyncio import Redis

from ..config import db_settings

token_blacklist=Redis(host=db_settings.REDIS_HOST,port=db_settings.REDIS_PORT,db=0)


async def add_jti_to_blacklist(jti:str):
    print('uuuu')
    await token_blacklist.set(jti,"blacklist")

async def check_is_jti(jti:str)->bool:
    return await token_blacklist.exists(jti)