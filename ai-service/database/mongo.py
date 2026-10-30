import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config.settings import settings

logger = logging.getLogger("travelsync.mongo")

_client: AsyncIOMotorClient | None = None

def get_mongo_client() -> AsyncIOMotorClient:
    """Return a singleton Motor client, initializing on first use."""
    global _client
    if _client is None:
        logger.info(f"Initializing Motor client with URI {settings.DATABASE_URL}")
        _client = AsyncIOMotorClient(settings.DATABASE_URL)
    return _client

async def get_mongo_db() -> AsyncIOMotorDatabase:
    """FastAPI dependency that yields the default database.
    Usage: `db: AsyncIOMotorDatabase = Depends(get_mongo_db)`
    """
    client = get_mongo_client()
    # Motor's get_default_database respects the DB name in the URI.
    return client.get_default_database()
