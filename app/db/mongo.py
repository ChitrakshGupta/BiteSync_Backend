from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


class MongoDB:
    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None


mongodb = MongoDB()


async def connect_to_mongo() -> None:
    mongodb.client = AsyncIOMotorClient(settings.mongodb_uri)
    mongodb.db = mongodb.client[settings.mongodb_db_name]


async def close_mongo_connection() -> None:
    if mongodb.client:
        mongodb.client.close()
