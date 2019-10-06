#!/usr/bin/env python

import bme680
import time

import json
import urllib3.request


print("""indoor-air-quality.py - Estimates indoor air quality.

Runs the sensor for a burn-in period, then uses a
combination of relative humidity and gas resistance
to estimate indoor air quality as a percentage.

Press Ctrl+C to exit!

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
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# start_time and curr_time ensure that the
# burn_in_time (in seconds) is kept track of.

http = urllib3.PoolManager()

def collect_aq():
    start_time = time.time()
    curr_time = time.time()
    burn_in_time = 300

    burn_in_data = []

    try:
        # Collect gas resistance burn-in values, then use the average
        # of the last 50 values to set the upper limit for calculating
        # gas_baseline.
        print('Collecting gas resistance burn-in data for 5 mins\n')
        while curr_time - start_time < burn_in_time:
            curr_time = time.time()
            if sensor.get_sensor_data() and sensor.data.heat_stable:
                gas = sensor.data.gas_resistance
                burn_in_data.append(gas)
                print('Gas: {0} Ohms'.format(gas))
                time.sleep(1)

        gas_baseline = sum(burn_in_data[-50:]) / 50.0

        # Set the humidity baseline to 40%, an optimal indoor humidity.
        hum_baseline = 40.0

        # This sets the balance between humidity and gas reading in the
        # calculation of air_quality_score (25:75, humidity:gas)
        hum_weighting = 0

        print('Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n'.format(
            gas_baseline,
            hum_baseline))

        while True:
            if sensor.get_sensor_data() and sensor.data.heat_stable:
                gas = sensor.data.gas_resistance
                hum = sensor.data.humidity
                gas_offset = gas_baseline - gas


                # Calculate gas_score as the distance from the gas_baseline.
                
                gas_score = (gas / gas_baseline)
                gas_score *= 100 

                # Calculate air_quality_score.
                air_quality_score = gas_score

                data = [
                    {
                        "location_id": 7,
                        "type": "airquality",
                        "source_type": "local_bme680",
                        "value": round(air_quality_score, 2)
                    } 
                ]               

                jsondata = json.dumps(data).encode('utf-8')
                req = http.request('POST','http://192.168.0.10:5000/add_sensors_data',
                body=jsondata,headers={'Content-Type': 'application/json'})


                
                print('Gas: {0:.2f} Ohms,humidity: {1:.2f} %RH,air quality: {2:.2f}'.format(
                    gas,
                    hum,
                    air_quality_score))

                return

    except KeyboardInterrupt:
        pass

data = [
        {
            "location_id": 7,
            "type": "airquality",
            "source_type": "local_bme680",
            "value": round(22, 2)
        } 
]               



while True:
    collect_aq()
    time.sleep(300)