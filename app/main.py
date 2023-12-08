from fastapi import FastAPI

from router.bookings_router import booking_router
from router.clients_router import client_router
from utils.mongo_utils import connect_and_init_mongo, close_mongo_connect

app = FastAPI()

app.include_router(booking_router, tags=['Booking'], prefix='/api/bookings')
app.include_router(client_router, tags=['Client'], prefix='/api/clients')
app.add_event_handler("startup", connect_and_init_mongo)
app.add_event_handler("shutdown", close_mongo_connect)
