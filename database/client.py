from pymongo import AsyncMongoClient
from config import Config


async def get_client():
    client = AsyncMongoClient(Config.MONGO)
    return client


async def get_database():
    client = await get_client()
    return client[Config.MONGO_DATABASE_NAME]
