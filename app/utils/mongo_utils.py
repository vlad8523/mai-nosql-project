import asyncio
import os

from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from bson import ObjectId

from models.client import Client
from models.room import Room
from models.booking import Booking

db_client: AsyncIOMotorClient = None


async def get_clients_collection() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection = os.getenv('CLIENTS_COLLECTION')

    return db_client.get_database(mongo_db).get_collection(mongo_collection)


async def get_rooms_collection() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection = os.getenv('ROOMS_COLLECTION')

    return db_client.get_database(mongo_db).get_collection(mongo_collection)


async def get_bookings_collection() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection = os.getenv('BOOKINGS_COLLECTION')

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
    except Exception as ex:
        print(f'Cant connect to mongo: {ex}')


def close_mongo_connect():
    global db_client
    if db_client is None:
        return
    db_client.close()


def map_client(client: Any) -> Client:
    return Client(id=str(client['_id']),
                  name=client['name'])


def map_room(room: Any) -> Room:
    return Room(id=str(room['_id']),
                address=room['address'],
                description=room['description'],
                attributes=room['attributes'])


def map_booking(booking: Any) -> Booking:
    return Booking(id=str(booking['_id']),
                   room_id=booking['room_id'],
                   client_id=booking['client_id'],
                   booking_start=booking['booking_start'],
                   booking_end=booking['booking_end'],
                   booking_status=booking['booking_status'])


def get_filter(_id: str) -> dict:
    return {'_id': ObjectId(_id)}
