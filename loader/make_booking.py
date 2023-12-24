import pymongo
from bson import ObjectId
from random import choice
from datetime import datetime, timedelta
import json, random, time
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

for client in clients:
    client["_id"] = str(client["_id"])

for room in rooms:
    room["_id"] = str(room["_id"])

array = []
current_datetime = datetime.today() - timedelta(days=random.randint(1, 10))
next_day = current_datetime + timedelta(days=random.randint(1, 10))
# Генерация записей в таблице booking
for i in range(10000):  # Например, создадим 10 записей
    client_id = choice(clients)["_id"]
    room_id = choice(rooms)["_id"]
    #booking_dates = [
    #    (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),  # Дата начала брони (на завтра)
    #    (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")   # Дата окончания брони (послезавтра)
    #]
    booking_start = int(time.mktime(current_datetime.timetuple()))
    booking_end = int(time.mktime(next_day.timetuple()))
    booking_status = choice(["booked", "paid", "free"])

    # Вставка записи в таблицу booking
    array.append({
        "client_id": client_id,
        "room_id": room_id,
        "booking_dates": {
            "gte": booking_start,
            "lt": booking_end
        },
        "booking_status": booking_status
    })
#booking_collection.insert_many(array)
with open(r"data_loader/bookings.json", "w") as file:
    # file.write(str(array))
    json.dump(array, file)

print("Записи успешно добавлены в таблицу booking.")
