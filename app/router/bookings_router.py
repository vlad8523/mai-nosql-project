from typing import Any

from fastapi import APIRouter, Depends, status
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from starlette.responses import Response

# from models.booking import Booking, UpdateBookingModel
# from utils.mongo_utils import get_bookings_collection, map_booking, get_filter

booking_router = APIRouter()


@booking_router.get("/")
async def hello_world():
    return "Hello world"
