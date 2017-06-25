import json
import sqlite3

import pytz
from dateutil.parser import parse
from datetime import date, datetime, time
from babel.dates import format_date, format_datetime, format_time
from urllib.request import urlopen


db = sqlite3.connect('data/data.sqlite')

c = db.cursor()
url = "http://api.openweathermap.org/data/2.5/weather?q=Zagreb,hr&appid=cd778955a5c3757c5d056f8ed83aea3c&units=metric"
weather = json.loads(urlopen(url).read().decode('utf-8'))

time = datetime.fromtimestamp(weather['dt'], pytz.timezone('UTC')).isoformat()
queryTemperature = "REPLACE INTO temperature (source_id, value,time) VALUES(?, ?, ?)"
queryHumidity = "REPLACE INTO humidity (source_id, value,time) VALUES(?, ?, ?)"
queryPressure = "REPLACE INTO pressure (source_id, value,time) VALUES(?, ?, ?)"
queryWindspeed = "REPLACE INTO windspeed (source_id, value,time) VALUES(?, ?, ?)"
source_temperature = "5"
source_humidity = "6"
source_pressure = "7"
source_windspeed = "8"
c.execute(queryTemperature, [source_temperature, weather['main']['temp'], time])
c.execute(queryHumidity, [source_humidity, weather['main']['humidity'], time])
c.execute(queryPressure, [source_pressure, weather['main']['pressure'], time])
c.execute(queryWindspeed, [source_pressure, weather['wind']['speed'], time])

db.commit()
db.close()


