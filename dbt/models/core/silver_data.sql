{{ config(
      materialized='incremental',
      unique_key='date_day'
      partition_by={
        "field": "time",
        "data_type": "timestamp",
        "granularity": "day"
      }
  ) }}

SELECT
row_Key,
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
FROM
    {{ ref('bronze_data') }}

{% if is_incremental() %}

  -- this filter will only be applied on an incremental run
  where time >= (select max(time) from {{ this }})

{% endif %}