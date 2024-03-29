
import urllib.request
import json
from datetime import datetime
from dateutil import tz
from dateutil import parser

req = urllib.request.Request('http://localhost:8123/api/states')
req.add_header('Content-Type', 'application/json')
req.add_header('Authorization','Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI0ZThhMzUzMTQ4Y2M0OThhOWIzZTAyZGFhMTNmNTIwYiIsImlhdCI6MTYzNTMzMzg4NSwiZXhwIjoxOTUwNjkzODg1fQ.9qLj90QnN3IPoBHDxTeUXNK2x1AwSgj_SK025_u_Kkg')

#jsondata = json.dumps(data)
#jsondataasbytes = jsondata.encode('utf-8')
response = urllib.request.urlopen(req)

from_zone = tz.tzutc()
to_zone = tz.tzlocal()


sensors = {
    'sensor.a4c1389591fd_humidity': {'location_id': 7, 'source_type': 'mith2-bedroom', 'type': 'humidity'},
    'sensor.a4c1389591fd_temperature': {'location_id': 7, 'source_type': 'mith2-bedroom', 'type': 'temperature'},

    'sensor.0x158d0006b27de7_humidity': {'location_id': 7, 'source_type': 'aqara-attic', 'type': 'humidity'},
    'sensor.0x158d0006b27de7_temperature': {'location_id': 7, 'source_type': 'aqara-attic', 'type': 'temperature'},

    'sensor.a4c138927b06_temperature': {'location_id': 7, 'source_type': 'mith2-kids', 'type': 'temperature'},
    'sensor.a4c138927b06_humidity': {'location_id': 7, 'source_type': 'mith2-kids', 'type': 'humidity'},

    'sensor.a4c1382e9b94_humidity': {'location_id': 7, 'source_type': 'mith2-study', 'type': 'humidity'},
    'sensor.a4c1382e9b94_temperature': {'location_id': 7, 'source_type': 'mith2-study', 'type': 'temperature'},

    'sensor.a4c138f616bb_humidity': {'location_id': 7, 'source_type': 'mith2-living', 'type': 'humidity'},
    'sensor.a4c138f616bb_temperature': {'location_id': 7, 'source_type': 'mith2-living', 'type': 'temperature'},

    'sensor.a4c138178771_humidity': {'location_id': 7, 'source_type': 'mith2-bathroom', 'type': 'humidity'},
    'sensor.a4c138178771_temperature': {'location_id': 7, 'source_type': 'mith2-bathroom', 'type': 'temperature'},

    'sensor.a4c138ea2857_humidity': {'location_id': 7, 'source_type': 'mith2-frontdoor', 'type': 'humidity'},
    'sensor.a4c138ea2857_temperature': {'location_id': 7, 'source_type': 'mith2-frontdoor', 'type': 'temperature'},

    'sensor.a4c13862e5a9_humidity': {'location_id': 7, 'source_type': 'mith2-garage', 'type': 'humidity'},
    'sensor.a4c13862e5a9_temperature': {'location_id': 7, 'source_type': 'mith2-garage', 'type': 'temperature'},

    'sensor.a4c138d38173_humidity': {'location_id': 7, 'source_type': 'mith2-cellar', 'type': 'humidity'},
    'sensor.a4c138d38173_temperature': {'location_id': 7, 'source_type': 'mith2-cellar', 'type': 'temperature'},
}

r = response.read()
json_r = json.loads(r.decode(response.info().get_param('charset') or 'utf-8'))
print (r)

post_items = []
for item in json_r:
    if item['entity_id'] in sensors and item['state'] != 'unavailable':
        utc = parser.parse(item['last_updated'])

        # Tell the datetime object that it's in UTC time zone since 
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)

        # Convert time zone
        local = utc.astimezone(to_zone)
        post_items.append( {
            "location_id": sensors[item['entity_id']]['location_id'],
            "source_type": sensors[item['entity_id']]['source_type'],
            "type": sensors[item['entity_id']]['type'],
#            "logged_at": local.isoformat(),
            'value': item['state']
        })
        #print (local.isoformat(), item['state'])

req = urllib.request.Request('http://vedranrodic.com:5000/add_sensors_data')
req.add_header('Content-Type', 'application/json')
jsondata = json.dumps(post_items)
#print(jsondata)
jsondataasbytes = jsondata.encode('utf-8')
response = urllib.request.urlopen(req, jsondataasbytes)


