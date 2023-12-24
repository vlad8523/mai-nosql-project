import json

# Чтение имен из файла users.json
with open("C:/Users/Rabinowitz/Desktop/nosql_db/mai-nosql-project/loader/data_loader/users.json", "r", encoding="utf-8") as input_file:
    names = [((line.replace(',', '')).replace('"', '')).strip() for line in input_file]

# Создание списка словарей для каждого имени
data = [{"name": name} for name in names]

# Запись данных в новый JSON файл
with open("UsersNew.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=2)
