from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from utils.mongo_utils import get_bookings_collection, get_filter, map_booking
from models.booking import Booking, UpdateBookingModel


class RepositoryBooking:
    _db_collection: AsyncIOMotorCollection

    def __init__(self, db_collection: AsyncIOMotorCollection):
        self._db_collection = db_collection

    async def create_booking(self, booking: UpdateBookingModel) -> str:
        insert_result = await self._db_collection.insert_one(dict(booking))
        return str(insert_result.inserted_id)

    async def get_all(self) -> list[Booking]:
        db_bookings = []
        async for booking in self._db_collection.find():
            db_bookings.append(map_booking(booking))
        return db_bookings

    async def get_by_id(self, booking_id: str) -> Booking | None:
        print(f'Get booking {booking_id} from mongo')
        db_booking = await self._db_collection.find_one(get_filter(booking_id))
        return map_booking(db_booking)

    async def update(self, booking_id: str, booking: UpdateBookingModel) -> Booking | None:
        db_booking = await self._db_collection.find_one_and_replace(get_filter(booking_id), dict(booking))
        return map_booking(db_booking)

    async def delete(self, booking_id: str) -> Booking | None:
        db_booking = await self._db_collection.find_one_and_delete(get_filter(booking_id))
        return map_booking(db_booking)

    @staticmethod
    def get_instance(db_collection: AsyncIOMotorCollection = Depends(get_bookings_collection)):
        return RepositoryBooking(db_collection)
