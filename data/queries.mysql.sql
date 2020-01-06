select * from pm10;

select * from source;

select
year(time),MONTH(time),avg(value) 
from pm10 
where month(time)=12 and source_id=1
group by 1,2; 


select
year(time),avg(value) 
from pm10 
where  source_id=1
group by 1; 