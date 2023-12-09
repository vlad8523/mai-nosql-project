from typing import List
from pydantic import BaseModel

from models.room import Room
from models.client import Client


class Booking(BaseModel):
    id: str
    room_id: Room
    client_id: Client
    booking_dates: List[str]
    booking_status: str


class CreateBookingModel(BaseModel):
    room_id: str
    client_id: str
    booking_dates: List[str]
    booking_status: str


class UpdateBookingModel(BaseModel):
    client_id: str
    booking_dates: List[str]
    booking_status: str
