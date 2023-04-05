SERVICE_ACCOUNT_JSON_PATH = '.google\credentials\google_credentials.json'
GCP_PROJECT_ID = 'dezoomcamp-375819'
GCP_GCS_BUCKET = f'earthquakes_data_lake_{GCP_PROJECT_ID}'
BQ_DATASET_STAGING = 'earthquake_stg'
BQ_DATASET_PROD = 'earthquake_prod'
GCS_URL = f'gs://{GCP_GCS_BUCKET}'

