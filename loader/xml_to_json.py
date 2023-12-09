import xmltodict
import json

with open('C:/Users/Rabinowitz/Desktop/nosql_db/mai-nosql-project/data/Users.xml') as xml_file:
    data_dict = xmltodict.parse(xml_file.read())
    json_data = json.dumps(data_dict, indent=2)

with open('Users.json', 'w') as json_file:
    json_file.write(json_data)
