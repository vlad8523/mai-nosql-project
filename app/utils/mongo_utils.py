import asyncio
import os

from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from bson import ObjectId

from models.client import Client

db_client: AsyncIOMotorClient = None


async def get_clients_collection() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection = os.getenv('CLIENTS_COLLECTION')

    return db_client.get_database(mongo_db).get_collection(mongo_collection)


async def connect_and_init_mongo():
    global db_client
    mongo_uri = os.getenv('MONGO_URI')
    mongo_db = os.getenv('MONGO_DB')
    clients_collection = os.getenv('CLIENTS_COLLECTION')
    rooms_collection = os.getenv('ROOMS_COLLECTION')
    bookings_collection = os.getenv('BOOKINGS_COLLECTION')
    try:
        db_client = AsyncIOMotorClient(mongo_uri)
        await db_client.server_info()
        print(f'Connected to mongo with uri {mongo_uri}')

        create_clients_collection_future = db_client.get_database(mongo_db). \
            create_collection(clients_collection)

        create_bookings_collection_future = db_client.get_database(mongo_db). \
            create_collection(bookings_collection)

        create_rooms_collection_future = db_client.get_database(mongo_db). \
            create_collection(rooms_collection)

        if mongo_db not in await db_client.list_database_names():
            await asyncio.gather(create_clients_collection_future,
                                 create_bookings_collection_future,
                                 create_rooms_collection_future)
    except Exception as ex:
        print(f'Cant connect to mongo: {ex}')


def close_mongo_connect():
    global db_client
    if db_client is None:
        return
    db_client.close()


def map_client(client: Any) -> Client:
    return Client(id=str(client['_id']), name=client['name'])


def get_filter(_id: str) -> dict:
    return {'_id': ObjectId(_id)}
