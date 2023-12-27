import json
import os

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from typing import Dict

from models.booking import UpdateBookingModel, Booking
from utils.elasticsearch_utils import get_elasticsearch_client


class SearchBookingRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __init__(self, index: str, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = index

    async def create(self, booking_id: str, booking: UpdateBookingModel):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=booking_id, document=dict(booking))

    async def update(self, booking_id: str, booking: UpdateBookingModel):
        await self._elasticsearch_client.update(index=self._elasticsearch_index, id=booking_id, doc=dict(booking))

    async def delete(self, booking_id: str):
        await self._elasticsearch_client.delete(index=self._elasticsearch_index, id=booking_id)

    async def find_by_room(self, room_id: str):
        index_exist = await self._elasticsearch_client.indices.exists(index=self._elasticsearch_index)

        if not index_exist:
            return []

        query = {
            "match": {
                "room_id": {
                    "query": room_id
                }
            }
        }

        responses = await self._elasticsearch_client.search(index=self._elasticsearch_index,
                                                            query=query)
        if 'hits' not in responses.body:
            return []
        result = responses.body['hits']['hits']

        print(result)
        bookings = list(map(lambda booking: Booking(id=booking['_id'],
                                                    room_id=booking['_source']['room_id'],
                                                    client_id=booking['_source']['client_id'],
                                                    booking_dates=booking['_source']['booking_dates'],
                                                    booking_status=booking['_source']['booking_status']), result))

        return bookings

    async def find_by_date(self, booking_date: Dict[str, int]):
        index_exist = await self._elasticsearch_client.indices.exists(index=self._elasticsearch_index)

        if not index_exist:
            return []

        query = {
            "range": {
                "booking_date": booking_date
            }
        }

        responses = await self._elasticsearch_client.search(index=self._elasticsearch_index,
                                                            query=query)

        print(responses)
        if 'hits' not in responses.body:
            return []

    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = os.getenv('BOOKING_INDEX')
        return SearchBookingRepository(elasticsearch_index, elasticsearch_client)
