from typing import Any

from fastapi import APIRouter, Depends, status
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from starlette.responses import Response

from models.room import Room, UpdateRoomModel
from utils.mongo_utils import get_rooms_collection, map_room, get_filter

room_router = APIRouter()


@room_router.post("/")
async def add_Room(Room: UpdateRoomModel,
                     db_collection: AsyncIOMotorCollection = Depends(get_rooms_collection)) -> str:
    insert_result = await db_collection.insert_one(dict(Room))
    return str(insert_result.inserted_id)


@room_router.put("/{room_id}", response_model=Room)
async def update_student(room_id: str, Room_model: UpdateRoomModel,
                         db_collection: AsyncIOMotorCollection = Depends(get_rooms_collection)) -> Any:
    if not ObjectId.is_valid(room_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    student = await db_collection.find_one_and_replace(get_filter(room_id), dict(Room_model))
    if student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return map_room(student)


@room_router.get("/")
async def get_all_Rooms(db_collection: AsyncIOMotorCollection = Depends(get_rooms_collection)):
    db_Rooms = []
    async for Room in db_collection.find():
        db_Rooms.append(map_room(Room))
    return db_Rooms


@room_router.get("/{room_id}", response_model=Room)
async def get_by_id(room_id: str, db_collection: AsyncIOMotorCollection = Depends(get_rooms_collection)) -> Any:
    if not ObjectId.is_valid(room_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_student = await db_collection.find_one(get_filter(room_id))
    if db_student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return map_room(db_student)


@room_router.delete("/{room_id}")
async def remove_student(room_id: str,
                         db_collection: AsyncIOMotorCollection = Depends(get_rooms_collection)) -> Response:
    if not ObjectId.is_valid(room_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_student = await db_collection.find_one_and_delete(get_filter(room_id))
    if db_student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response()
