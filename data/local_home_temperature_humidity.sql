insert into location (name) values ('my_apartment');

insert into source (location_id, type, source_type) values ('3','temperature','local_dht22');
insert into source (location_id, type, source_type) values ('3','humidity','local_dht22');
select * from source;
