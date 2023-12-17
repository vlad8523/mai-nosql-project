import asyncio

from utils.mongo_utils import connect_and_init_mongo, close_mongo_connect

from utils.elasticsearch_utils import connect_and_init_elasticsearch, close_elasticsearch_connect


async def startup():
    init_mongo_future = connect_and_init_mongo()
    init_elasticsearch_future = connect_and_init_elasticsearch()
    await asyncio.gather(init_mongo_future, init_elasticsearch_future)


async def shutdown():
    close_mongo_connect()
    await close_elasticsearch_connect()
