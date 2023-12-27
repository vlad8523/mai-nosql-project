from typing import Dict
from pydantic import BaseModel


class Booking(BaseModel):
    id: str
    room_id: str
    client_id: str
    booking_dates: Dict[str, int]
    booking_status: str


class UpdateBookingModel(BaseModel):
    room_id: str
    client_id: str
    booking_dates: Dict[str, int]
    booking_status: str
