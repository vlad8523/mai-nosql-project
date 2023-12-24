import json
import os

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from models.room import UpdateRoomModel, Room
from utils.elasticsearch_utils import get_elasticsearch_client


class SearchRoomRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __init__(self, index: str, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = index

    async def create(self, room_id: str, room: UpdateRoomModel):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=room_id, document=dict(room))

    async def create(self, room_id: str, room: UpdateRoomModel):
        await self._elasticsearch_client.update(index=self._elasticsearch_index, id=room_id, doc=dict(room))

    async def delete(self, room_id: str):
        await self._elasticsearch_client.delete(index=self._elasticsearch_index, id=room_id)

    async def find_by_address(self, address: str):
        index_exist = await self._elasticsearch_client.indices.exists(index=self._elasticsearch_index)

        if not index_exist:
            return []

        query = {
            "match": {
                "address": {
                    "query": address
                }
            }
        }

        responses = await self._elasticsearch_client.search(index=self._elasticsearch_index,
                                                            query=query,
                                                            filter_path=['hits.hits._id', 'hits.hits._source'])
        if 'hits' not in responses.body:
            return []
        result = responses.body['hits']['hits']
        rooms = list(map(lambda room: Room(id=room['_id'],
                                           address=room['_source']['address'],
                                           description=room['_source']['description'],
                                           attributes=json.loads(room['_source']['attributes'])), result))
        return rooms

    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = os.getenv('ROOM_INDEX')
        return SearchRoomRepository(elasticsearch_index, elasticsearch_client)