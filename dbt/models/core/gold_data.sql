{{ config(materialized='table') }}

with tbl_data as (
select row_Key,
,time	
,latitude	
,longitude	
,depth	
,mag	
,magType	
,nst	
,gap	
,dmin	
,rms	
,net	
,id	
,updated	
,place	
,type	
,horizontalError	
,depthError	
,magError	
,magNst	
,status	
,locationSource	
,magSource 
from {{ ref('silver_data') }}
)
    select 
    date_trunc(time, year) as _year, 
    date_trunc(time, month) as _month, 
    date_trunc(time, day) as _day,

    count(*) earthquakes_total_count, 

    max(depth) max_depth,
    max(mag) max_mag,

    avg(depth) avg_depth,
    avg(mag) avg_mag,

    from tbl_data
    group by 1,2,3
