from typing import Any

from fastapi import APIRouter

from models.booking import Booking

booking_router = APIRouter()


@booking_router.get("/")
async def hello_world():
    return "Hello world"
