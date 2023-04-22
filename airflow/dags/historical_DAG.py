# from google.cloud import storage, bigquery
# from google.cloud.exceptions import NotFound

from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
import os
from config import GCS_ID

GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
GCP_GCS_BUCKET = os.environ.get('GCP_GCS_BUCKET')
BQ_DATASET_STAGING = os.environ.get('BIGQUERY_DATASET', 'earthquake_stg')

EXECUTION_MONTH = '{{ logical_date.strftime("%-m") }}'
EXECUTION_DAY = '{{ logical_date.strftime("%-d") }}'
EXECUTION_HOUR = '{{ logical_date.strftime("%-H") }}'
EXECUTION_DATETIME_STR = '{{ logical_date.strftime("%m%d%H") }}'


MACRO_VARS = {"GCP_PROJECT_ID":GCP_PROJECT_ID, 
              "BIGQUERY_DATASET": BQ_DATASET_STAGING, 
              "EXECUTION_DATETIME_STR": EXECUTION_DATETIME_STR
              }

def print_hello():
    return 'Hello world from first Airflow DAG!'

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

dag = DAG('hello_world', description='Daily DAG',
          schedule_interval='5 * * * *',
          start_date=datetime(2023, 4, 1),
          catchup=False,
          user_defined_macros=MACRO_VARS)

hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)

hello_operator