# from google.cloud import storage, bigquery
# from google.cloud.exceptions import NotFound

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
import os
# from config import GCS_ID

GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
GCP_GCS_BUCKET = os.environ.get('GCP_GCS_BUCKET')
BQ_DATASET_STAGING = os.environ.get('BIGQUERY_DATASET', 'earthquake_stg')
START_YEAR = int(os.getenv("START_YEAR", "2022"))

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

MACRO_VARS = {"GCP_PROJECT_ID": GCP_PROJECT_ID, "BIGQUERY_DATASET": BQ_DATASET_STAGING,
        "EXECUTION_DATETIME_STR": EXECUTION_DATETIME_STR}



def print_hello():
    print(file_name)
    print(dataset_url)
    print(local_file_path)
    print(GCP_PROJECT_ID)
    print(GCP_GCS_BUCKET)
    print(BQ_DATASET_STAGING)
    print(EXECUTION_DATETIME_STR)
    return 'Hello world from first Airflow DAG!'


dag = DAG('Spark_DAG', description='Spark_DAG Test',
        schedule_interval='5 * * * *',
        start_date=datetime(2023, 4, 22),
        catchup=False,
        user_defined_macros=MACRO_VARS)

hello_operator = PythonOperator(
        task_id='hello_task', python_callable=print_hello, dag=dag)

pwd_task = BashOperator(
        task_id='print_dir',
        bash_command='ls /opt/airflow/dags/'
        )

execute_spark_task = BashOperator(
        task_id='spark_job_run',
        bash_command='python /opt/airflow/dags/spark_job.py'
        )

hello_operator >> pwd_task >> execute_spark_task

