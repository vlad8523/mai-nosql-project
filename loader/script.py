import asyncio
import json
from elasticsearch import AsyncElasticsearch
import pandas as pd
import os
import pymongo
from bson import ObjectId
from random import choice
from datetime import datetime, timedelta
from copy import deepcopy

def get_data(file_name: str):
    data: pd.DataFrame = pd.read_excel(f'{file_name}')
    data: pd.DataFrame = pd.DataFrame(data.dropna())
    data = data.reset_index(drop=True)
    data_dict: dict = data.to_dict('index')
    data_values = list(data_dict.values())
    with open(f'{file_name}.json', 'w') as file:
        file_json = json.dumps(data_values)
        file.write(file_json)


async def load_data(file_name, index):

    # Подключение к MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["booking-db"]

    # Получение коллекций
    db_collection = database[index]
    #rooms_collection = database["rooms"]
    #booking_collection = database["bookings"]

    # Считываем инфу из файла
    with open(f'{file_name}', 'r') as objs_json:
         objs = json.load(objs_json)
         #print(objs[1])
    # Вставлвяем в монгу
    print('Начали вставку в монгу')
    try:
        objs_mongo = deepcopy(objs)
        #print(objs_mongo[0])
        insert_result = db_collection.insert_many(objs_mongo)
        #print(objs_mongo[0])
        mapped_to_str_ids = list(map(str, insert_result.inserted_ids))
        print('Успешно вставили в монгу')
    except Exception as e:
        print(e)
    
    elasticsearch_client = None
    elasticsearch_uri = ['http://localhost:9200']
    try:
        elasticsearch_client = AsyncElasticsearch(elasticsearch_uri)
        await elasticsearch_client.info()
        print(f'Connected to elasticsearch with uri {elasticsearch_uri}')
    except Exception as ex:
        print(f'Cant connect to elasticsearch: {ex}')

    bulk = []
    for i in range(len(objs)):
        #print(objs[i])
        index_operation = {
            'index': {'_index': index, '_id': mapped_to_str_ids[i]}}
        bulk.append(index_operation)
        bulk.append(objs[i])
    chunk_size = 1000
    chunks = [bulk[i:i + chunk_size]
              for i in range(0, len(bulk), chunk_size)]
    
    
    print("Пытаемся вставить в эластик")
    for i in range(len(chunks)):
        await elasticsearch_client.bulk(operations=chunks[i])
        print(f"Chunk {i} of added")
    print("Успешно вставили в эластик")


#get_data("loader\data_loader\listings.xlsx")
asyncio.run(load_data("loader\data_loader\listings.xlsx.json", "rooms"))
