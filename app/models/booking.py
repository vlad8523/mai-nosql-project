from typing import List
from pydantic import BaseModel


class Booking(BaseModel):
    room_id: str
    client_id: str
    booking_dates: List[str]
    booking_status: str


class UpdateBookingModel(BaseModel):
    client_id: str
    booking_dates: List[str]
    booking_status: str
