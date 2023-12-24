import os
import asyncio
from elasticsearch import AsyncElasticsearch
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
import pymongo
elasticsearch_client: AsyncElasticsearch = None


def get_elasticsearch_client() -> AsyncElasticsearch:
    return elasticsearch_client


async def connect_and_init_elasticsearch():
    global elasticsearch_client
    elasticsearch_uri = 'http://localhost:9200'
    try:
        elasticsearch_client = AsyncElasticsearch(elasticsearch_uri)
        await elasticsearch_client.info()
        print(f'Connected to elasticsearch with uri {elasticsearch_uri}')
    except Exception as ex:
        print(f'Cant connect to elasticsearch: {ex}')


async def close_elasticsearch_connect():
    global elasticsearch_client
    if elasticsearch_client is None:
        return
    await elasticsearch_client.close()

def insert_to_elastic():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["booking-db"]

    # Получение     коллекций   
    clients_collection = database["clients"]
    rooms_collection = database["rooms"]
    booking_collection = database["bookings"]

    clients = list(clients_collection.find())
    rooms = list(rooms_collection.find())
    bookings = list(booking_collection.find())
    print(rooms[0])

async def main():
    await connect_and_init_elasticsearch()

insert_to_elastic()
#asyncio.run(main=main())