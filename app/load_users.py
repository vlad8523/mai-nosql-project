import xml.etree.ElementTree as ET
import requests


def extract_displayed_names(xml_file_path):
    displayed_names = []

    # Парсим XML файл
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Итерируем по элементам и добавляем значения DisplayName в список
    for item in root.findall('.//row'):
        displayed_names.append(item.get('DisplayName'))

    return displayed_names

# Пример использования
xml_file_path = './mai-nosql-project/data/Users.xml'
displayed_names_list = extract_displayed_names(xml_file_path)

# Выводим список
print(displayed_names_list)

# URL, на который будет отправлен запрос
url = 'http://localhost:8000/api/clients'

# Данные, которые вы хотите отправить (в формате словаря)
for name in displayed_names_list:
    params = {
        'name': name
    }

    response = requests.post(url, params=params)

    # Печать статус-кода и ответа сервера
    print(f'Status Code: {response.status_code}')
    print('Response:')
    print(response.text)
