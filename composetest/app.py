import redis
from flask import Flask
import json
import xml.etree.ElementTree as ET


app = Flask(__name__)
client = redis.Redis(host='redis', port=6379)

def xml_to_dict(xml_element):
    result = {}
    for element in xml_element:
        if element.tag not in result:
            result[element.tag] = []
        result[element.tag].append(xml_to_dict(element) if len(element) else element.text)
    return result

def xml_to_json(xml_string):
    xml_element = ET.fromstring(xml_string)
    data_dict = xml_to_dict(xml_element)
    json_string = json.dumps(data_dict)
    return json_string

@app.route('/')
def hello():
    xml_file=open("config.xml","r")
    xml_string=xml_file.read()
    parsedData = xml_to_json(xml_string)
    print(parsedData)
    client.set('doc', parsedData)

    return client.get('doc')

