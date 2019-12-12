#!/usr/bin/env python3
import mh_z19
import time
import datetime
import json
import urllib.request

try:
    with mh_z19.MH_Z19("/dev/ttyUSB0") as con:
        co2 = con.get()
        print(str(datetime.datetime.today()) + "\t" + str(co2) + " ppm", flush=True)
        data = [
            {
                "location_id": 3,
                "type": "co2",
                "source_type": "local_mh-z19b",
                "value": round(co2, 2)
            }
        ]

        req = urllib.request.Request('http://localhost:5000/add_sensors_data')
        req.add_header('Content-Type', 'application/json')
        jsondata = json.dumps(data)
        jsondataasbytes = jsondata.encode('utf-8')
        response = urllib.request.urlopen(req, jsondataasbytes)


except KeyboardInterrupt:
    print("Interruption.")
