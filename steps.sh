pip install --upgrade google-cloud-storage
pip install --upgrade google-cloud-bigquery

export GCP_PROJECT_ID="dezoomcamp-375819"
export GCP_GCS_BUCKET="earthquakes_data_lake_dezoomcamp-375819"

docker-compose build
docker-compose up airflow-init
docker-compose up

docker-compose ps

## On finishing your run or to shut down the container/s:
docker-compose down

## To stop and delete containers, delete volumes with database data, and download images, run:
docker-compose down --volumes --rmi all
docker-compose down --volumes --remove-orphans

docker exec -it --user airflow airflow-airflow-scheduler-1 bash -c "ls /opt/spark/python/lib"
docker exec -it --user airflow airflow-airflow-scheduler-1 bash -c "python /opt/airflow/dags/spark_job.py"

docker exec -it --user airflow airflow-airflow-scheduler-1 bash -c "ls /opt/airflow/lib"

docker exec -it --user airflow airflow-airflow-scheduler-1 bash -c "gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar ./lib/gcs-connector-hadoop3-2.2.5.jar"

docker exec -it --user airflow airflow-airflow-scheduler-1 bash -c "gsutil cp gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar ./lib/spark-bigquery-latest_2.12.jar"
