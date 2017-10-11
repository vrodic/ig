import sys


import json
import urllib2

import subprocess
cmdpipe = subprocess.Popen("/home/vedran/WiringOP/dht", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
result = {}
row =cmdpipe.stdout.readline()
if ':' in row:
    humidity,temperature = row.split(':')

if humidity is not None and temperature is not None:
    humidity = float(humidity)
    temperature = float(temperature)
    data = [
        {
            "location_id": 5,
            "type": "temperature",
            "source_type": "local_dht22",
            "value": round(temperature, 2)
        },
        {
            "location_id": 5,
            "type": "humidity",
            "source_type": "local_dht22",
            "value": round(humidity, 2)
        }
    ]
    
    try:
        req = urllib2.Request('http://app.address:5000/add_sensors_data')
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, json.dumps(data))
    except:
        pass

