from typing import List
from pydantic import BaseModel

class Room(BaseModel):
    id: int
    address: str
    description: str
    attributes: List[str]

class UpdateRoomModel(BaseModel):
  address: str
    description: str
    attributes: List[str]
