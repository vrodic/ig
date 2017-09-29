import json
import pymysql.cursors

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


def import_source(source):
    source_id = str(source['id'])
    type = source['type']
    url_template = source['url_template']

    c = db.cursor()
    tablename = type


    c.execute("SELECT time FROM " + tablename + " WHERE source_id= " + source_id + " ORDER BY time DESC LIMIT 1")
    last_time = c.fetchone()

    if last_time is None:
        start_date_hr = '01.01.2000.'
    else:
        start_date_hr = format_date(last_time['time'], format='short', locale='hr_HR')

    print(start_date_hr)

    end_date_hr = format_date(datetime.now(), format='short', locale='hr_HR')
    url = url_template.replace('{{startdate_hr}}', start_date_hr)
    url = url.replace('{{enddate_hr}}', end_date_hr)
    print(url)

    aq = json.loads(urlopen(url).read().decode('utf-8'))

    for item in aq:
        val = item['Podatak']
        time = val['vrijeme']
        value = val['vrijednost']
        print(item)
        query = "REPLACE INTO " + tablename + " (source_id, value,time) VALUES(" + source_id + ", " + str(value) + ",'" + time + "')"
        c.execute(query)

    db.commit()


c.execute("SELECT * FROM source WHERE source_type='croatian_air_quality'")
for source in c.fetchall():
    print(source)
    import_source(source)

db.close()




