# pip install py-sds011 
import datetime
import json
import urllib.request

import sds011
import time

sensor = sds011.SDS011("/dev/ttyUSB0", use_query_mode=True)
sensor.sleep(sleep=False)
time.sleep(5)
pm25, pm10 = sensor.query()
print(pm25, pm10)

data = [
        {   
            "location_id": 3,
            "type": "pm25",
            "source_type": "localsds011",
            "value": round(pm25, 2)
        },
        {   
            "location_id": 3,
            "type": "pm10",
            "source_type": "localsds011",
            "value": round(pm10, 2)
        },

]

req = urllib.request.Request('http://vedranrodic.com:5000/add_sensors_data')
req.add_header('Content-Type', 'application/json')
jsondata = json.dumps(data)
jsondataasbytes = jsondata.encode('utf-8')
response = urllib.request.urlopen(req, jsondataasbytes)

sensor.sleep()
