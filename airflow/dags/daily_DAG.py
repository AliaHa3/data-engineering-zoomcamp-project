from google.cloud import storage, bigquery
from google.cloud.exceptions import NotFound
import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
import os
import json


GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
GCP_GCS_BUCKET = os.environ.get('GCP_GCS_BUCKET')
BQ_DATASET_STAGING = os.environ.get('BIGQUERY_DATASET', 'earthquake_stg')
SERVICE_ACCOUNT_JSON_PATH = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
external_table_name = 'daily_staging'

EXECUTION_MONTH = '{{ logical_date.strftime("%-m") }}'
EXECUTION_DAY = '{{ logical_date.strftime("%-d") }}'
EXECUTION_HOUR = '{{ logical_date.strftime("%-H") }}'
EXECUTION_DATETIME_STR = '{{ logical_date.strftime("%m%d%H") }}'

current_date = datetime.now()
currentSecond = current_date.second
currentMinute = current_date.minute
currentHour = current_date.hour
currentDay = current_date.day
currentMonth = current_date.month
currentYear = current_date.year

past_date = datetime.now() - timedelta(hours=1)
pastSecond = past_date.second
pastMinute = past_date.minute
pastHour = past_date.hour
pastDay = past_date.day
pastMonth = past_date.month
pastYear = past_date.year

starttime = f"{pastYear}-{pastMonth:02}-{pastDay:02}T{pastHour:02}:{pastMinute:02}:{pastSecond:02}"
endtime = f"{currentYear}-{currentMonth:02}-{currentDay:02}T{currentHour:02}:{currentMinute:02}:{currentSecond:02}"
timestamp = str(datetime.now()).replace(
    "-", "").replace(":", "").replace(" ", "")[:14]
file_name = f'data_{starttime.replace("-","").replace(":","")}_{endtime.replace("-","").replace(":","")}_{timestamp}'
dataset_url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={starttime}&endtime={endtime}"
local_file_path = f"/opt/airflow/data/{file_name}.csv.gz"


# dag = DAG('hourly_DAG', description='Hourly DAG', schedule_interval='5 * * * *',
#   start_date=datetime(2023, 4, 22), catchup=False, max_active_runs=1, user_defined_macros=MACRO_VARS)

def extract_data_to_local(url, file_name, **kwargs):
    df = pd.read_csv(url)
    print(df.head())

    # local_file_path = f"{data_folder_path}/{file_name}.csv.gz"

    # df.to_parquet(path,index=False, compression="gzip")
    df.to_csv(local_file_path, index=False, compression="gzip")

    kwargs['ti'].xcom_push(key="general", value={"local_file_path": local_file_path,
                                                 "file_name": file_name})
                                                 
    # return {"local_file_path": local_file_path, "file_name": file_name}

def upload_to_bucket(**kwargs):
    print(kwargs)
    print(kwargs['ti'])
    dict_data = kwargs['ti'].xcom_pull(key="general",task_ids="extract_data_to_local_task")
    # print(xcom_data)
    # dict_data = json.loads(xcom_data)
    # print(dict_data)

    local_file_path = dict_data['local_file_path']
    blob_name = f"earthquakes/{dict_data['file_name']}.csv.gz"

    """ Upload data to a bucket"""
    storage_client = storage.Client.from_service_account_json(
        SERVICE_ACCOUNT_JSON_PATH)

    bucket = storage_client.get_bucket(GCP_GCS_BUCKET)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_file_path)

    kwargs['ti'].xcom_push(key="general2", value=dict_data)
    
    # returns a public url
    # return ti


def execute_query(query_str):
    """ create table in BigQuery"""
    bigquery_client = bigquery.Client.from_service_account_json(
        SERVICE_ACCOUNT_JSON_PATH)
    query_job = bigquery_client.query(query_str)

    results = query_job.result()  # Waits for job to complete
    print(results)
    return results


def check_table_exists(table_name):
    """ check if table exists in BigQuery"""
    try:
        bigquery_client = bigquery.Client.from_service_account_json(
            SERVICE_ACCOUNT_JSON_PATH)
        result = bigquery_client.get_table(table_name)
    except NotFound:
        print(f" Table {table_name} is not found")
        result = None
    return result


def create_external_table(table_name, **kwargs):
    print(kwargs)
    print(kwargs['ti'])
    dict_data = kwargs['ti'].xcom_pull(key="general2",task_ids="local_to_gcs_task")
    print(dict_data)
    # dict_data = json.loads(xcom_data)
    # print(dict_data)

    file_name = dict_data['file_name']

    is_exist = check_table_exists(
        f'{GCP_PROJECT_ID}.{BQ_DATASET_STAGING}.{table_name}')
    if is_exist is None:
        query_str = f"""
        CREATE OR REPLACE EXTERNAL TABLE `{GCP_PROJECT_ID}.{BQ_DATASET_STAGING}.{table_name}`
        OPTIONS (
        format = 'CSV',
        uris = ['gs://{GCP_GCS_BUCKET}/earthquakes/{file_name}.csv.gz']
        )
        """
        result = execute_query(query_str)
    
    kwargs['ti'].xcom_push(key="general3", value=dict_data)
    # return ti


def print_hello():
    print(file_name)
    print(dataset_url)
    print(local_file_path)
    print(GCP_PROJECT_ID)
    print(GCP_GCS_BUCKET)
    print(BQ_DATASET_STAGING)
    print(EXECUTION_DATETIME_STR)
    return 'Hello world from first Airflow DAG!'


dag = DAG('hourly_DAG', description='Hourly DAG', schedule_interval='5 * * * *',
          start_date=datetime(2023, 4, 22), catchup=False, max_active_runs=1)

extract_data_to_local_task = PythonOperator(
    task_id=f"extract_data_to_local_task",
    python_callable=extract_data_to_local,
    provide_context=True,
    dag=dag,
    op_kwargs={
        "url": dataset_url,
        "file_name": file_name
    }
)

local_to_gcs_task = PythonOperator(
    task_id=f"local_to_gcs_task",
    python_callable=upload_to_bucket,
    provide_context=True,
    dag=dag
)

clear_local_files_task = BashOperator(
    task_id=f"clear_local_files_task",
    bash_command="rm {{ ti.xcom_pull(key='general3',task_ids='gcs_to_bq_external_task')['local_file_path'] }}",
    dag=dag
)

gcs_to_bq_external_task = PythonOperator(
    task_id=f"gcs_to_bq_external_task",
    python_callable=create_external_table,
    provide_context=True,
    dag=dag,
    op_kwargs={
        "table_name": f"{external_table_name}"
    }
)

extract_data_to_local_task >> local_to_gcs_task >> gcs_to_bq_external_task >> clear_local_files_task
