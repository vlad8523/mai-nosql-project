from typing import Any

from fastapi import APIRouter, Depends, status
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from starlette.responses import Response

from models.room import Room, UpdateRoomModel
from repository.repository_rooms import RepositoryRooms
from repository.search_repository_rooms import SearchRoomRepository
from utils.mongo_utils import get_rooms_collection, map_room, get_filter
from typing import List

room_router = APIRouter()


@room_router.post("/")
async def add_room(room: UpdateRoomModel,
                   db_collection: AsyncIOMotorCollection = Depends(get_rooms_collection)) -> str:
    insert_result = await db_collection.insert_one(dict(room))
    return str(insert_result.inserted_id)


@room_router.put("/{room_id}", response_model=Room)
async def update_room(room_id: str, room_model: UpdateRoomModel,
                      db_collection: AsyncIOMotorCollection = Depends(get_rooms_collection)) -> Any:
    if not ObjectId.is_valid(room_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    room = await db_collection.find_one_and_replace(get_filter(room_id), dict(room_model))
    if room is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return map_room(room)


@room_router.get("/")
async def get_all_rooms(repository: RepositoryRooms = Depends(RepositoryRooms.get_instance)):
    return await repository.get_all()


@room_router.get("/filter")
async def get_by_address(address: str,
                         repository: SearchRoomRepository = Depends(SearchRoomRepository.get_instance)) -> Any:
    return await repository.find_by_address(address)


@room_router.get("/{room_id}", response_model=Room)
async def get_by_id(room_id: str, db_collection: AsyncIOMotorCollection = Depends(get_rooms_collection)) -> Any:
    print("get_by_id")
    if not ObjectId.is_valid(room_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_room = await db_collection.find_one(get_filter(room_id))
    if db_room is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return map_room(db_room)


@room_router.post("/attributes")
async def get_by_attributes(attributes: List[str],
                            repository: SearchRoomRepository = Depends(SearchRoomRepository.get_instance)):
    return await repository.find_by_attributes(attributes)


@room_router.delete("/{room_id}")
async def remove_room(room_id: str,
                      db_collection: AsyncIOMotorCollection = Depends(get_rooms_collection)) -> Response:
    if not ObjectId.is_valid(room_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_room = await db_collection.find_one_and_delete(get_filter(room_id))
    if db_room is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response()
