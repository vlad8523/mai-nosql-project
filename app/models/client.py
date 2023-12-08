from typing import List
from pydantic import BaseModel

class Client(BaseModel):
    id: int
    name: str

class UpdateClientModel(BaseModel):
    name: str