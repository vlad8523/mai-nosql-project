from typing import List
from pydantic import BaseModel

class Booking(BaseModel):
    room_id: int
    client_id: int
    booking_dates: List[str]
    booking_status: str
  
class UpdateBookingModel(BaseModel):
    client_id: int
    booking_dates: List[str]
    booking_status: str