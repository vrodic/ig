import json
import pymysql.cursors

import pytz
from dateutil.parser import parse
from datetime import date, datetime, time, timedelta
from babel.dates import format_date, format_datetime, format_time
from urllib.request import urlopen


db = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='wlog',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

c = db.cursor()

apiKey = "???"
baseUrl = "http://api.wunderground.com/api/"+ apiKey+ "/history_"
zagrebUrl = "zmw:00000.1.14236.json"

dt = datetime(2017, 6, 13)
end = datetime(2017, 6, 24, 15, 40, 59)

#dt = datetime(2016, 10, 1)
#end = datetime(2016, 11, 11, 15, 40, 59)

step = timedelta(days=1)

while dt < end:  
    dt += step
    dateString =dt.strftime('%Y%m%d')
    url = baseUrl + dateString + "/q/" + zagrebUrl

    weather = json.loads(urlopen(url).read().decode('utf-8'))
    print("Read observations for " + dateString)

    observations = weather['history']['observations']
    for hour in observations:
        #print(hour)
        time = hour['utcdate']['year'] + '-' + hour['utcdate']['mon'] + '-' + hour['utcdate']['mday'] + ' ' + hour['utcdate']['hour'] + ':' + hour['utcdate']['min']
        temp = hour['tempm']

        queryTemperature = "REPLACE INTO temperature (source_id, value,time) VALUES(5, "+ str(hour['tempm'])+", '"+time+"')"
        if (hour['hum']):
            queryHumidity = "REPLACE INTO humidity (source_id, value,time) VALUES(6, "+ str(hour['hum'])+", '"+time+"')"
            c.execute(queryHumidity)
        if (hour['pressurem']):
            queryPressure = "REPLACE INTO pressure (source_id, value,time) VALUES(7, "+ str(hour['pressurem'])+", '"+time+"')"
            c.execute(queryPressure)
        queryWindspeed = "REPLACE INTO windspeed (source_id, value,time) VALUES(8, "+ str(hour['wspdm'])+", '"+time+"')"
        
        c.execute(queryTemperature)
        

        c.execute(queryWindspeed)
        db.commit()




db.close()


