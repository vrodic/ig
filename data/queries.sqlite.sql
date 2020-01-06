select * from source;
select * from pm10 where source_id=1 order by time desc limit 10;
/* average pm10 monthlyfor source_id 1*/
select strftime('%Y-%m', time), avg(value)
from pm10
where source_id=1
group by strftime('%Y-%m', time)
 order by time desc;

/* drill down to month of interest */
select strftime('%Y-%m-%d', time), avg(value)
from pm10
where source_id= 1 and strftime('%Y-%m', time)='2017-01'
group by strftime('%Y-%m-%d', time)
 order by time desc;




/* drill down to date of interest */
select time, value
from pm10
where source_id= 1 and strftime('%Y-%m-%d', time)='2017-01-23'
 order by time desc;

select year(time) from pm10;
select count(*) from pm10;
select count(*) from pm10 where source_id=2;
select count(*) from humidity;

select * from temperature where strftime('%H',time) = '10' order by time desc;


select strftime('%Y-%m', time), avg(value)
from temperature
where source_id=3 and strftime('%H', time) = '00'
group by strftime('%Y-%m', time)
 order by time desc;

/* drill down to month of interest */
select strftime('%Y-%m-%d', time), avg(value)
from temperature
where source_id= 3 and strftime('%Y-%m', time)='2017-01'
group by strftime('%Y-%m-%d', time)
 order by time desc;

select * from temperature order by value asc limit 100;

/* drill down to date of interest */
select time, value
from temperature
where source_id= 3 and strftime('%Y-%m-%d', time)='2017-05-01' and strftime('%H', time) = '12'
 order by time desc;