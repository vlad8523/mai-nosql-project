from typing import Dict
from pydantic import BaseModel

from models.room import Room
from models.client import Client


class Booking(BaseModel):
    id: str
    room_id: str
    client_id: str
    booking_dates: Dict[str, int]
    booking_status: str


class CreateBookingModel(BaseModel):
    room_id: str
    client_id: str
    booking_dates: Dict[str, int]
    booking_status: str


class UpdateBookingStatus(BaseModel):
    booking_status: str
