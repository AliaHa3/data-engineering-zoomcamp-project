from google.cloud import storage, bigquery
from google.cloud.exceptions import NotFound
import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
import os


GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
GCP_GCS_BUCKET = os.environ.get('GCP_GCS_BUCKET')
BQ_DATASET_PROD = os.environ.get('BIGQUERY_DATASET', 'earthquake_prod')

SERVICE_ACCOUNT_JSON_PATH = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
external_table_name = 'daily_staging'

EXECUTION_MONTH = '{{ logical_date.strftime("%-m") }}'
EXECUTION_DAY = '{{ logical_date.strftime("%-d") }}'
EXECUTION_HOUR = '{{ logical_date.strftime("%-H") }}'
EXECUTION_DATETIME_STR = '{{ logical_date.strftime("%m%d%H") }}'

def extract_past_year(years,**kwargs):
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    past_year_data = []
    for y in years:
        for m in months:            
            start_year = y
            start_month = m
            start_day = 1
            start_hour = 0
            start_minute = 0
            start_second = 0

            end_year = y
            end_month = m
            end_day = 31
            end_hour = 23
            end_minute = 59
            end_second = 59

            starttime = f"{start_year}-{start_month:02}-{start_day:02}T{start_hour:02}:{start_minute:02}:{start_second:02}"
            endtime =  f"{end_year}-{end_month:02}-{end_day:02}T{end_hour:02}:{end_minute:02}:{end_second:02}"

            
            try:
                dataset_url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={starttime}&endtime={endtime}"
                print(dataset_url)
                df = pd.read_csv(dataset_url)
                past_year_data.append(df)
            except Exception as e:
                print(str(e))

    past_year_df= pd.concat(past_year_data)
    file_name = "historical_data"
    local_file_path = f"/opt/airflow/data/{file_name}.csv.gz"
    
    past_year_df.to_csv(local_file_path, index=False, compression="gzip")

    kwargs['ti'].xcom_push(key="general", value={"local_file_path": local_file_path,
                                                 "file_name": file_name})


def upload_to_bucket(**kwargs):
    print(kwargs)
    print(kwargs['ti'])
    dict_data = kwargs['ti'].xcom_pull(key="general",task_ids="extract_data_to_local_task")


    local_file_path = dict_data['local_file_path']
    blob_name = f"earthquakes/{dict_data['file_name']}.csv.gz"

    """ Upload data to a bucket"""
    storage_client = storage.Client.from_service_account_json(
        SERVICE_ACCOUNT_JSON_PATH)

    bucket = storage_client.get_bucket(GCP_GCS_BUCKET)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_file_path)

    dict_data["bucket_file_path"] = f"gs://{GCP_GCS_BUCKET}/{blob_name}"
    kwargs['ti'].xcom_push(key="general2", value=dict_data)
    


dag = DAG('historical_DAG', description='Historical DAG', schedule_interval='@once',
          start_date=datetime(2023, 4, 22), catchup=False, max_active_runs=1)

extract_data_to_local_task = PythonOperator(
    task_id=f"extract_data_to_local_task",
    python_callable=extract_past_year,
    provide_context=True,
    dag=dag,
    op_kwargs={
        "years": [2020,2021,2022,2023]
    }
)

local_to_gcs_task = PythonOperator(
    task_id=f"local_to_gcs_task",
    python_callable=upload_to_bucket,
    provide_context=True,
    dag=dag
)

spark_transformation_task = BashOperator(
    task_id=f"spark_transformation_task",
    bash_command="python /opt/airflow/dags/spark_job.py --input_file '{{ ti.xcom_pull(key='general2',task_ids='local_to_gcs_task')['bucket_file_path']}}' ",
    dag=dag
)

clear_local_files_task = BashOperator(
    task_id=f"clear_local_files_task",
    bash_command="rm {{ ti.xcom_pull(key='general2',task_ids='local_to_gcs_task')['local_file_path'] }}",
    dag=dag
)


extract_data_to_local_task >> local_to_gcs_task >> spark_transformation_task >> clear_local_files_task
