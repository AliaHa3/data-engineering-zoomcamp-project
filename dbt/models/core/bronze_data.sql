{{ config(materialized = 'table') }}

SELECT {{ dbt_utils.surrogate_key(['id']) }} AS row_Key,
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
     {{ source('staging', 'raw_data') }}