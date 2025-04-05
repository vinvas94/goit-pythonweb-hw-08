import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"


async def init_rate_limiter(app: FastAPI):
    redis_instance = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_instance)
