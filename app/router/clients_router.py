from typing import Any

from fastapi import APIRouter, Depends, status
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from starlette.responses import Response

from models.client import Client, UpdateClientModel
from utils.mongo_utils import get_clients_collection, map_client, get_filter

client_router = APIRouter()


@client_router.post("/")
async def add_client(client: UpdateClientModel,
                     db_collection: AsyncIOMotorCollection = Depends(get_clients_collection)) -> str:
    insert_result = await db_collection.insert_one(dict(client))
    return str(insert_result.inserted_id)


@client_router.put("/{client_id}", response_model=Client)
async def update_student(client_id: str, client_model: UpdateClientModel,
                         db_collection: AsyncIOMotorCollection = Depends(get_clients_collection)) -> Any:
    if not ObjectId.is_valid(client_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    student = await db_collection.find_one_and_replace(get_filter(client_id), dict(client_model))
    if student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return map_client(student)


@client_router.get("/")
async def get_all_clients(db_collection: AsyncIOMotorCollection = Depends(get_clients_collection)):
    db_clients = []
    async for client in db_collection.find():
        db_clients.append(map_client(client))
    return db_clients


@client_router.get("/{client_id}", response_model=Client)
async def get_by_id(client_id: str, db_collection: AsyncIOMotorCollection = Depends(get_clients_collection)) -> Any:
    if not ObjectId.is_valid(client_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_student = await db_collection.find_one(get_filter(client_id))
    if db_student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return map_client(db_student)


@client_router.delete("/{client_id}")
async def remove_student(client_id: str,
                         db_collection: AsyncIOMotorCollection = Depends(get_clients_collection)) -> Response:
    if not ObjectId.is_valid(client_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_student = await db_collection.find_one_and_delete(get_filter(client_id))
    if db_student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response()
