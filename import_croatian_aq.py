import json
import sqlite3


from dateutil.parser import parse
from datetime import date, datetime, time
from babel.dates import format_date, format_datetime, format_time
from urllib.request import urlopen


db = sqlite3.connect('data/data.sqlite')

c = db.cursor()


def import_source(source):
    source_id = str(source[0])
    type = source[2]
    url_template = source[5]

    c = db.cursor()
    tablename = type

    last_time = \
        c.execute("SELECT time FROM " + tablename + " WHERE source_id=? ORDER BY time DESC LIMIT 1", [source_id])\
        .fetchone()

    if last_time is None:
        start_date_hr = '01.01.2000.'
    else:
        start_date_hr = format_date(parse(last_time[0]), format='short', locale='hr_HR')

    print(start_date_hr)

    end_date_hr = format_date(datetime.now(), format='short', locale='hr_HR')
    url = url_template.replace('{{startdate_hr}}', start_date_hr)
    url = url.replace('{{enddate_hr}}', end_date_hr)
    print(url)

    query = "REPLACE INTO " + tablename + " (source_id, value,time) VALUES(?, ?, ?)"
    print(query)
    aq = json.loads(urlopen(url).read().decode('utf-8'))

    for item in aq:
        val = item['Podatak']
        time = val['vrijeme']
        value = val['vrijednost']
        print(item)
        c.execute(query, [source_id, value, time])

    db.commit()


for source in c.execute("SELECT * FROM source WHERE source_type='croatian_air_quality'"):
    print(source)
    import_source(source)

db.close()




