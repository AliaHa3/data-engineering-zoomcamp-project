pip install --upgrade google-cloud-storage
pip install --upgrade google-cloud-bigquery

export GCP_PROJECT_ID="dezoomcamp-375819"
export GCP_GCS_BUCKET="earthquakes_data_lake_dezoomcamp-375819"


docker exec -it --user airflow airflow-airflow-scheduler-1 bash -c "ls /opt/spark/python/lib"