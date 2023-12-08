from typing import List
from pydantic import BaseModel


class Client(BaseModel):
    id: str
    name: str


class UpdateClientModel(BaseModel):
    name: str
