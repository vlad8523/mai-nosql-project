# import xmltodict
# import json

# with open('loader/data_loader/Users.xml', 'r', encoding='utf-8') as xml_file:
#     data_dict = xmltodict.parse(xml_file.read())
#     json_data = json.dumps(data_dict, indent=2)

# with open('users.json', 'w') as json_file:
#     json_file.write(json_data)

import xmltodict
import json

with open('data_loader/Users.xml', 'r', encoding='utf-8') as xml_file:
    data_dict = xmltodict.parse(xml_file.read())

# Извлечь только содержимое ключа 'DisplayName'
display_names = [entry['@DisplayName'] for entry in data_dict['users']['row']]

# Создать новый словарь с ключом 'displayName' и списком значений
filtered_data = {'displayName': display_names}

# Преобразовать в JSON
json_data = json.dumps(filtered_data, ensure_ascii=False)

with open('data_loader/users.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)
