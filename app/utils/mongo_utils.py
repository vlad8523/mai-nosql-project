import os

from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from models.client import Client

db_client: AsyncIOMotorClient = None

async def get_client_collection() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection = 'clients'

    return db_client.get_database(mongo_db).get_collection(mongo_collection)

async def connect_and_init_mongo():
    global db_client
    mongo_uri = os.getenv('MONGO_URI')
    try:
        db_client = AsyncIOMotorClient(mongo_uri)
        await db_client.server_info()
        print(f'Connected to mongo with uri {mongo_uri}')
    except Exception as ex:
        print(f'Cant connect to mongo: {ex}')

def close_mongo_connect():
    global db_client
    if db_client is None:
        return
    db_client.close()
