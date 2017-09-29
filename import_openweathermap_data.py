import json
import pymysql.cursors

import pytz
from dateutil.parser import parse
from datetime import date, datetime, time
from babel.dates import format_date, format_datetime, format_time
from urllib.request import urlopen


db = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='wlog',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

c = db.cursor()

url = "http://api.openweathermap.org/data/2.5/weather?q=Zagreb,hr&appid=cd778955a5c3757c5d056f8ed83aea3c&units=metric"
weather = json.loads(urlopen(url).read().decode('utf-8'))

time = datetime.fromtimestamp(weather['dt'], pytz.timezone('UTC')).isoformat()
queryTemperature = "REPLACE INTO temperature (source_id, value,time) VALUES(5, "+ str(weather['main']['temp'])+", '"+time+"')"

queryHumidity = "REPLACE INTO humidity (source_id, value,time) VALUES(6, "+ str(weather['main']['humidity'])+", '"+time+"')"
queryPressure = "REPLACE INTO pressure (source_id, value,time) VALUES(7, "+ str(weather['main']['pressure'])+", '"+time+"')"
queryWindspeed = "REPLACE INTO windspeed (source_id, value,time) VALUES(8, "+ str(weather['wind']['speed'])+", '"+time+"')"
source_temperature = "5"
source_humidity = "6"
source_pressure = "7"
source_windspeed = "8"
print(time)
print(weather['main']['temp'])
c.execute(queryTemperature)
c.execute(queryHumidity)
c.execute(queryPressure)
c.execute(queryWindspeed)

db.commit()
db.close()


