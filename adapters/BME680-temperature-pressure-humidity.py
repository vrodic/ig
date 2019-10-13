#!/usr/bin/env python

import bme680
import time

import json
import urllib3.request

print("""temperature-pressure-humidity.py - Displays temperature, pressure, and humidity.

If you don't need gas readings, then you can read temperature,
pressure and humidity quickly.

Press Ctrl+C to exit

""")

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

http = urllib3.PoolManager()

read = False
print('Polling:')
try:
    while not read:        
        if sensor.get_sensor_data():
            output = '{0:.2f} C,{1:.2f} hPa,{2:.3f} %RH'.format(
                sensor.data.temperature,
                sensor.data.pressure,
                sensor.data.humidity)            
            print(output)
            #time.sleep(5)
            data = [
                {
                    "location_id": 7,
                    "type": "temperature",
                    "source_type": "local_bme680",
                    "value": round(sensor.data.temperature, 2)
                },
                {
                    "location_id": 7,
                    "type": "humidity",
                    "source_type": "local_bme680",
                    "value": round(sensor.data.humidity, 2)
                },
                {
                    "location_id": 7,
                    "type": "pressure",
                    "source_type": "local_bme680",
                    "value": round(sensor.data.pressure, 2)
                }

            ]               

            jsondata = json.dumps(data).encode('utf-8')
            req = http.request('POST','http://192.168.0.10:5000/add_sensors_data',
            body=jsondata,headers={'Content-Type': 'application/json'})
            read = True
        else:
            print "no data"            

except KeyboardInterrupt:
    pass
