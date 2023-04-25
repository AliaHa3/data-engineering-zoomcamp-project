# https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01T16:17:28&endtime=2014-01-02T16:17:28

# https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2014-01-01T16:17:28&endtime=2014-01-02T16:17:28


# wget https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2014-01-01T16:17:28&endtime=2014-01-02T16:17:28 test1.csv

# time	timestamp
# latitude	double
# longitude	double
# depth	double
# mag	double
# magType	string
# nst	double
# gap	double
# dmin	double
# rms	double
# net	string
# id	string
# updated	timestamp
# place	string
# type	string
# horizontalError	double
# depthError	double
# magError	double
# magNst	double
# status	string
# locationSource	string
# magSource	string


import pandas as pd
from pathlib import Path
from google.cloud import storage, bigquery
from google.cloud.exceptions import NotFound
import datetime
# from config import GCP_GCS_BUCKET,SERVICE_ACCOUNT_JSON_PATH,GCP_PROJECT_ID,BQ_DATASET_STAGING,BQ_DATASET_PROD,GCS_ID


# def extract_data_to_local(url,file_name,data_folder_path="data"):
#     df = pd.read_csv(url)
#     print(df.head())

#     local_file_path = f"{data_folder_path}/{file_name}.csv.gz"

#     # df.to_parquet(path,index=False, compression="gzip")
#     df.to_csv(local_file_path,index=False,compression="gzip")

#     return local_file_path


# def upload_to_bucket(blob_name, path_to_file, bucket_name=GCP_GCS_BUCKET):
#     """ Upload data to a bucket"""
#     storage_client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_JSON_PATH)

#     bucket = storage_client.get_bucket(bucket_name)
#     blob = bucket.blob(blob_name)
#     blob.upload_from_filename(path_to_file)
    
#     #returns a public url
#     return blob.public_url

# def execute_query(query_str):
#     """ create table in BigQuery"""
#     bigquery_client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON_PATH)
#     query_job = bigquery_client.query(query_str)

#     results = query_job.result()  # Waits for job to complete
#     print (results)
#     return results

# def check_table_exists(table_name):
#     """ check if table exists in BigQuery"""
#     try:
#         bigquery_client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON_PATH)
#         result = bigquery_client.get_table(table_name)
#     except NotFound:
#         print(f" Table {table_name} is not found")
#         result = None
#     return result


# def create_external_table(table_name):
#     is_exist = check_table_exists(f'{GCP_PROJECT_ID}.{BQ_DATASET_STAGING}.{table_name}')
#     if is_exist is None:
#         query_str = f"""
#         CREATE OR REPLACE EXTERNAL TABLE `{GCP_PROJECT_ID}.{BQ_DATASET_STAGING}.{table_name}`
#         OPTIONS (
#         format = 'CSV',
#         uris = ['gs://{GCS_ID}/earthquakes/*.csv.gz']
#         )
#         """
#         result = execute_query(query_str)
#     return result


# table_name = 'earthquakes_bronze'
# create_external_table(table_name)

#################################

# years = [2022]
# months = [1,2,3,4,5,6,7,8,9,10,11,12]

# years = [2019]
# months = [1]

# for y in years:
#     for m in months:            
#         start_year = y
#         start_month = m
#         start_day = 1
#         start_hour = 0
#         start_minute = 0
#         start_second = 0

#         end_year = y
#         end_month = m
#         end_day = 31
#         end_hour = 23
#         end_minute = 59
#         end_second = 59

#         starttime = f"{start_year}-{start_month:02}-{start_day:02}T{start_hour:02}:{start_minute:02}:{start_second:02}"
#         endtime =  f"{end_year}-{end_month:02}-{end_day:02}T{end_hour:02}:{end_minute:02}:{end_second:02}"

#         timestamp = str(datetime.datetime.now()).replace("-","").replace(":","").replace(" ","")[:14]
        
#         try:

#             file_name = f'data_{starttime.replace("-","").replace(":","")}_{endtime.replace("-","").replace(":","")}_{timestamp}'
#             dataset_url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={starttime}&endtime={endtime}"
#             local_file_path = extract_data_to_local(dataset_url,file_name,data_folder_path="data")
#             upload_to_bucket(f"earthquakes/{file_name}.csv.gz", local_file_path)
#         except Exception as e:
#             print(str(e))


from geopy.geocoders import Nominatim
from geopy.point import Point
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent="geoapiEnrichment")
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

def country_enrichment(row):
    # location = geolocator.reverse(Point(row['latitude'],row['longitude']))
    location = reverse(Point(row['latitude'],row['longitude']))
    address = {}
    if location is not None:
        address = location.raw['address']

    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    country_code = address.get('country_code', '')
    zipcode = address.get('postcode', '')

    row['city'] = city
    row['state'] = state
    row['country'] = country
    row['country_code'] = country_code
    row['zipcode'] = zipcode

    return row

df = pd.read_csv('data\data_20140101T161728_20140101T181728_20230326012042.csv.gz', compression='gzip', header=0)
print(df.head())


new_df = df.apply(country_enrichment, axis=1)
print(new_df.head())
new_df.to_csv('t.csv',index=False) #,compression="gzip"

# for i,row in df.iterrows():
#     print(row)
#     latitude = "25.594095"
#     longitude = "85.137566"
#     print(Point(row['latitude'],row['longitude']))
    

#     if i==10:
#         break



