from fastapi import FastAPI
from dotenv import load_dotenv

from router.bookings_router import booking_router
from utils.mongo_utils import connect_and_init_mongo, close_mongo_connect

load_dotenv()

app = FastAPI()

app.include_router(booking_router, tags=["Booking"], prefix="/api/bookings")
app.add_event_handler("startup", connect_and_init_mongo)
app.add_event_handler("shutdown", close_mongo_connect)
