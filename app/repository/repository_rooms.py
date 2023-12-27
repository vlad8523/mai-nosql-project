from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from utils.mongo_utils import get_rooms_collection, get_filter, map_room
from models.room import Room, UpdateRoomModel


class RepositoryRooms:
    _db_collection: AsyncIOMotorCollection

    def __init__(self, db_collection: AsyncIOMotorCollection):
        self._db_collection = db_collection

    async def create_room(self, room: UpdateRoomModel):
        insert_result = await self._db_collection.insert_one(dict(room))
        return insert_result

    async def get_all(self) -> list[Room]:
        db_rooms = []
        async for room in self._db_collection.find():
            db_rooms.append(map_room(room))
        return db_rooms

    async def get_by_id(self, room_id: str) -> Room | None:
        print(f'Get room {room_id} from mongo')
        db_room = await self._db_collection.find_one(get_filter(room_id))
        return map_room(db_room)

    async def update(self, room_id: str, room: UpdateRoomModel) -> Room | None:
        db_room = await self._db_collection.find_one_and_replace(get_filter(room_id), dict(room))
        return map_room(db_room)

    async def delete(self, room_id: str) -> Room | None:
        db_room = await self._db_collection.find_one_and_delete(get_filter(room_id))
        return map_room(db_room)

    @staticmethod
    def get_instance(db_collection: AsyncIOMotorCollection = Depends(get_rooms_collection)):
        return RepositoryRooms(db_collection)
