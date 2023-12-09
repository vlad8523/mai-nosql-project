from typing import Any

from fastapi import APIRouter, Depends, status
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from starlette.responses import Response

from models.booking import Booking, UpdateBookingModel, CreateBookingModel
from utils.mongo_utils import get_bookings_collection, map_booking, get_filter

booking_router = APIRouter()


@booking_router.post("/")
async def add_booking(booking: CreateBookingModel,
                      db_collection: AsyncIOMotorCollection = Depends(get_bookings_collection)) -> str:
    insert_result = await db_collection.insert_one(dict(booking))
    return str(insert_result.inserted_id)


@booking_router.put("/{booking_id}", response_model=Booking)
async def update_booking(booking_id: str, booking_model: UpdateBookingModel,
                         db_collection: AsyncIOMotorCollection = Depends(get_bookings_collection)) -> Any:
    if not ObjectId.is_valid(booking_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    booking = await db_collection.find_one_and_replace(get_filter(booking_id), dict(booking_model))
    if booking is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return map_booking(booking)


@booking_router.get("/")
async def get_all_bookings(db_collection: AsyncIOMotorCollection = Depends(get_bookings_collection)):
    db_bookings = []
    async for Room in db_collection.find():
        db_bookings.append(map_booking(Room))
    return db_bookings


@booking_router.get("/{booking_id}", response_model=Booking)
async def get_by_id(booking_id: str, db_collection: AsyncIOMotorCollection = Depends(get_bookings_collection)) -> Any:
    if not ObjectId.is_valid(booking_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_booking = await db_collection.find_one(get_filter(booking_id))
    if db_booking is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return map_booking(db_booking)


@booking_router.delete("/{booking_id}")
async def remove_booking(booking_id: str,
                         db_collection: AsyncIOMotorCollection = Depends(get_bookings_collection)) -> Response:
    if not ObjectId.is_valid(booking_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_booking = await db_collection.find_one_and_delete(get_filter(booking_id))
    if db_booking is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response()

