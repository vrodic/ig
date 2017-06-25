
CREATE TABLE location (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   name varchar(200),
   lat real,
   long real
);


drop table IF EXISTS source;
CREATE TABLE source(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  location_id integer,
  type varchar(200),
  source_type varchar(200),
  name varchar(200),
  url_template text
);

drop table IF EXISTS pm10;
create table pm10(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id integer,
  value real,
  time TIMESTAMP
);
create UNIQUE INDEX pm10u on pm10(time,source_id);

drop table IF EXISTS temperature;
create table temperature(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id integer,
  value real,
  time TIMESTAMP
);
create UNIQUE INDEX temperatureu on temperature(time,source_id);

drop table IF EXISTS humidity;
create table humidity(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id integer,
  value real,
  time TIMESTAMP
);
create UNIQUE INDEX humidityu on humidity(time,source_id);

/* croatian air quality data */
insert into location (name) values ('zagreb-2');

insert into source (location_id, type,source_type, name, url_template)
VALUES (1,'pm10','croatian_air_quality','pm10-zagreb2',
'http://iszz.azo.hr/iskzl/rs/podatak/export/json?postaja=156&polutant=5&tipPodatka=0&vrijemeOd={{startdate_hr}}&vrijemeDo={{enddate_hr}}');

insert into location (name) values ('zagreb-1');

insert into source (location_id, type,source_type, name, url_template)
VALUES (2,'pm10','croatian_air_quality','pm10-zagreb1',
'http://iszz.azo.hr/iskzl/rs/podatak/export/json?postaja=155&polutant=5&tipPodatka=0&vrijemeOd={{startdate_hr}}&vrijemeDo={{enddate_hr}}');

/* local data */
insert into location (name) values ('my_apartment');

insert into source (location_id, type, source_type) values ('3','temperature','local_dht22');
insert into source (location_id, type, source_type) values ('3','humidity','local_dht22');

insert into location (name, lat,long) values('zagreb-ow', '45.81', '15.98');
insert into source  (location_id, type, source_type, url_template)
values (4,'temperature', 'openweathermap', 'http://api.openweathermap.org/data/2.5/weather?q=Zagreb,hr&appid={{api_key}}&units=metric');

insert into source  (location_id, type, source_type)
values (4,'humidity', 'openweathermap');
insert into source  (location_id, type, source_type)
values (4,'pressure', 'openweathermap');

insert into source  (location_id, type, source_type)
values (4,'windspeed', 'openweathermap');

create table pressure(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id integer,
  value real,
  time TIMESTAMP
);
create UNIQUE INDEX pressureu on pressure(time,source_id);

create table windspeed(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id integer,
  value real,
  time TIMESTAMP
);
create UNIQUE INDEX windspeedu on windspeed(time,source_id);





