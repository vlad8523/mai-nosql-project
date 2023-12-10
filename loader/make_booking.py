import pymongo
from bson import ObjectId
from random import choice
from datetime import datetime, timedelta

# Подключение к MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["booking-db"]

# Получение коллекций
clients_collection = database["clients"]
rooms_collection = database["rooms"]
booking_collection = database["bookings"]

# Получение всех клиентов и комнат
clients = list(clients_collection.find())
rooms = list(rooms_collection.find())

# Генерация записей в таблице booking
for i in range(10000):  # Например, создадим 10 записей
    client_id = choice(clients)["_id"]
    room_id = choice(rooms)["_id"]
    booking_dates = [
        (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),  # Дата начала брони (на завтра)
        (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")   # Дата окончания брони (послезавтра)
    ]
    booking_status = choice(["0", "1"])

    # Вставка записи в таблицу booking
    booking_collection.insert_one({
        "client_id": client_id,
        "room_id": room_id,
        "booking_dates": booking_dates,
        "booking_status": booking_status
    })

print("Записи успешно добавлены в таблицу booking.")
