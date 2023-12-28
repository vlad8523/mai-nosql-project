from typing import Any, Dict

from fastapi import APIRouter, Depends, status
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from starlette.responses import Response

from models.booking import Booking, UpdateBookingModel
from repository.repository_booking import RepositoryBooking
from repository.repository_rooms import RepositoryRooms
from repository.search_repository_booking import SearchBookingRepository
from utils.mongo_utils import get_bookings_collection, map_booking, get_filter, map_booking_without_id, \
    get_clients_collection

from cache.memcached_utils import get_memcached_client
from pymemcache import HashClient

booking_router = APIRouter()


@booking_router.post("/")
async def add_booking(booking_model: UpdateBookingModel,
                      repository_booking: RepositoryBooking = Depends(RepositoryBooking.get_instance),
                      db_clients: AsyncIOMotorCollection = Depends(get_clients_collection),
                      repository_rooms: RepositoryRooms = Depends(RepositoryRooms.get_instance),
                      memcached_client: HashClient = Depends(get_memcached_client),
                      search_repository: SearchBookingRepository = Depends(SearchBookingRepository.get_instance)) -> str:

    db_client = await db_clients.find_one(get_filter(booking_model.client_id))

    if not db_client:
        return 'Client not found'

    db_room = await repository_rooms.get_by_id(booking_model.room_id)

    if not db_room:
        return 'Room not found'

    list_occupied_rooms = set(await search_repository.find_by_date(booking_model.booking_dates))

    print(list_occupied_rooms)
    print(booking_model.room_id)

    if booking_model.room_id not in list_occupied_rooms:
        booking_id = await repository_booking.create_booking(booking_model)
        memcached_client.add(booking_id, booking_model, expire=6000)
        return booking_id
    else:
        return 'Room is occupied'


@booking_router.post("/update")
async def update_status(booking_id: str,
                        repository: RepositoryBooking = Depends(RepositoryBooking.get_instance),
                        memcached_client: HashClient = Depends(get_memcached_client),
                        search_repository: SearchBookingRepository = Depends(
                            SearchBookingRepository.get_instance)) -> Response:
    if not ObjectId.is_valid(booking_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    db_booking = memcached_client.get(booking_id)

    if not db_booking:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    db_booking["booking_status"] = 'paid'

    await repository.update(booking_id, db_booking)

    if db_booking:
        await search_repository.create(booking_id, db_booking)

    memcached_client.delete(booking_id)

    return Response(status_code=status.HTTP_200_OK)


@booking_router.put("/{booking_id}", response_model=Booking)
async def update_booking(booking_id: str, booking_model: UpdateBookingModel,
                         db_collection: AsyncIOMotorCollection = Depends(get_bookings_collection)) -> Any:
    if not ObjectId.is_valid(booking_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    booking = await db_collection.find_one_and_replace(get_filter(booking_id), dict(booking_model))
    if booking is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return map_booking(booking)


@booking_router.get("/")
async def get_all_bookings(db_collection: AsyncIOMotorCollection = Depends(get_bookings_collection)):
    db_bookings = []
    async for Room in db_collection.find():
        db_bookings.append(map_booking(Room))
    return db_bookings


@booking_router.get("/room")
async def get_all_by_room_id(room_id: str,
                             search_repository: SearchBookingRepository = Depends(SearchBookingRepository.get_instance)):
    return await search_repository.find_by_room(room_id)


@booking_router.post("/date")
async def get_all_by_dates(dates: Dict[str, int],
                           search_repository: SearchBookingRepository = Depends(SearchBookingRepository.get_instance)):
    print(dates)
    return await search_repository.find_by_date(dates)


@booking_router.get("/{booking_id}", response_model=Booking)
async def get_by_id(booking_id: str,
                    db_collection: AsyncIOMotorCollection = Depends(get_bookings_collection),
                    memcached_client: HashClient = Depends(get_memcached_client)) -> Any:
    if not ObjectId.is_valid(booking_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    db_booking = memcached_client.get(booking_id)

    if db_booking is not None:
        return db_booking

    db_booking = await db_collection.find_one(get_filter(booking_id))

    if db_booking is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    memcached_client.add(booking_id, db_booking)

    return map_booking(db_booking)


@booking_router.delete("/{booking_id}")
async def remove_booking(booking_id: str,
                         db_collection: AsyncIOMotorCollection = Depends(get_bookings_collection)) -> Response:
    if not ObjectId.is_valid(booking_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_booking = await db_collection.find_one_and_delete(get_filter(booking_id))
    if db_booking is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response()
