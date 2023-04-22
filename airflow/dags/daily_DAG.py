# from google.cloud import storage, bigquery
# from google.cloud.exceptions import NotFound

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
import os
# from config import GCS_ID

GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
GCP_GCS_BUCKET = os.environ.get('GCP_GCS_BUCKET')
BQ_DATASET_STAGING = os.environ.get('BIGQUERY_DATASET', 'earthquake_stg')
table_name = 'raw_data'

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
local_file_path = f"data/{file_name}.csv.gz"

print (file_name)
print (dataset_url)
print (local_file_path)
print (GCP_PROJECT_ID)
print (GCP_GCS_BUCKET)
print (BQ_DATASET_STAGING)
print (EXECUTION_DATETIME_STR)

MACRO_VARS = {"GCP_PROJECT_ID": GCP_PROJECT_ID,
                              "BIGQUERY_DATASET": BQ_DATASET_STAGING,
                                                                  "EXECUTION_DATETIME_STR": EXECUTION_DATETIME_STR
                                                                                                                    }


def print_hello():
    print (file_name)
    print (dataset_url)
    print (local_file_path)
    print (GCP_PROJECT_ID)
    print (GCP_GCS_BUCKET)
    print (BQ_DATASET_STAGING)
    print (EXECUTION_DATETIME_STR)
    return 'Hello world from first Airflow DAG!'

dag = DAG('hello_world', description='Daily DAG',
                                  schedule_interval='5 * * * *',
                                                                  start_date=datetime(2023, 4, 22),
                                                                                                            catchup=False,
                                                                                                                                                                user_defined_macros=MACRO_VARS)
hello_operator = PythonOperator(
                            task_id='hello_task', python_callable=print_hello, dag=dag)
hello_operator

        # def extract_data_to_local(url,file_name):
            #     df = pd.read_csv(url)
                #     print(df.head())

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

                                                                                                                                                                            #  initate_dbt_task = BashOperator(
                                                                                                                                                                                #         task_id = 'dbt_initiate',
                                                                                                                                                                                    #         bash_command = 'cd /dbt && dbt deps && dbt seed --profiles-dir . --target prod'
                                                                                                                                                                                        #     )

                                                                                                                                                                                            #     execute_dbt_task = BashOperator(
                                                                                                                                                                                                #         task_id = 'dbt_streamify_run',
                                                                                                                                                                                                    #         bash_command = 'cd /dbt && dbt deps && dbt run --profiles-dir . --target prod'
                                                                                                                                                                                                        #     )

                                                                                                                                                                                                            ### #
                                                                                                                                                                                                                # create_external_table(table_name)
                                                                                                                                                                                                                    # extract_data_to_local(dataset_url,file_name)
                                                                                                                                                                                                                        # upload_to_bucket(f"earthquakes/{file_name}.csv.gz", local_file_path)
                                                                                                                                                                                                                            # initate_dbt_task
                                                                                                                                                                                                                                # execute_dbt_task
                                                                                                                                                                                                                                    

