import redis.asyncio as aioredis
from src.config import settings

token_blacklist = aioredis.StrictRedis(
    host=settings.redis_host, 
    port=settings.redis_port, 
    db=0, 
    decode_responses=True
)

async def add_jti_to_blacklist(jti: str):
    await token_blacklist.set(jti, "blacklisted", ex=settings.jti_expiration_seconds)

async def token_in_blacklist(jti: str) -> bool:
    result = await token_blacklist.exists(jti)
    return result == 1