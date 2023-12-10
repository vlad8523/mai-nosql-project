import pandas as pd
import json

# Чтение данных из Excel
excel_file = 'C:/Users/Rabinowitz/Desktop/nosql_db/mai-nosql-project/loader/data_loader/listings.xlsx'
df = pd.read_excel(excel_file)

# Замена NaN на пустую строку
df.fillna('', inplace=True)

# Преобразование данных в JSON формат
json_data = []
for index, row in df.iterrows():
    item = {
        "address": row['address'] if row['address'] is not None else "",
        "description": row['description'],
        "attributes": eval(row['attributes'])  # Используем eval для преобразования строки в список
    }
    json_data.append(item)

# Запись данных в JSON файл
json_file = 'Rooms.json'
with open(json_file, 'w', encoding='utf-8', errors='replace') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)


print(f"Данные успешно записаны в {json_file}")
