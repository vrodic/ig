# I have temp logger that logs like this
# /home/pi/Adafruit_Python_DHT/examples/AdafruitDHT.py 22 22 |gawk '{ print strftime("%Y-%m-%d %H:%M:%S"), $0; fflush(); }' >> accumulating_file

import sqlite3


from dateutil.parser import parse
from datetime import date, datetime, time
from babel.dates import format_date, format_datetime, format_time


db = sqlite3.connect('data/data.sqlite')

c = db.cursor()
queryTemperature = "REPLACE INTO temperature (source_id, value,time) VALUES(?, ?, ?)"
queryHumidity = "REPLACE INTO humidity (source_id, value,time) VALUES(?, ?, ?)"
source_temperature = "3"
source_humidity = "4"

for line in open('data/temp.log'):
    failed = line.find("Failed to get reading")
    if failed > 0:
        continue

    posTemp = line.find('Temp=')
    timestamp = line[0:posTemp].strip()

    posTemp = posTemp+5
    posTempEnd = line.find('*', posTemp)
    temperature = line[posTemp:posTempEnd]
    print(timestamp)
    print(temperature)
    posHumid = line.find('Humidity=') + 9
    posHumidEnd = line.find('%',posHumid)
    humidity = line[posHumid:posHumidEnd]
    print(humidity)
    #print(line.rstrip('\n'))
    c.execute(queryTemperature, [source_temperature, temperature, timestamp])
    c.execute(queryHumidity, [source_humidity, humidity, timestamp])

db.commit()
db.close()
