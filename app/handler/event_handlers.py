import asyncio

from utils.mongo_utils import connect_and_init_mongo, close_mongo_connect


async def startup():
    connect_and_init_mongo()


async def shutdown():
    close_mongo_connect()