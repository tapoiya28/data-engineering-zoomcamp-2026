import pandas as pd
import requests
import gzip
import io
from airflow.providers.google.cloud.hooks.gcs import GCSHook

import hashlib
import os

from airflow.sdk import get_current_context

prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases'


# BigQuery configuration
PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'dataengineer-zoomcamp-484202')
DATASET_ID = 'ny_taxi'
BUCKET_NAME = 'ny-taxi-data-lake'

def extract_yellow():
    context = get_current_context()
    data_start = context["data_interval_start"]
    year = data_start.year
    month = data_start.month

    # read csv
    filename = f'yellow_tripdata_{year}-{month:02}.csv.gz'
    url = f'{prefix}/download/yellow/{filename}'
    
    response = requests.get(url)
    response.raise_for_status()

    # decompress locally so bucket stores plain CSV
    with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as gz:
        decompressed_csv = gz.read()

    hook = GCSHook(gcp_conn_id='gcp-conn-id-1')
    bucket_name = BUCKET_NAME
    object_name = f"yellow/{filename.replace('.csv.gz', '.csv')}"
    print(object_name)
    hook.upload(bucket_name=bucket_name,
                object_name=object_name,
                mime_type='text/csv',
                data=decompressed_csv,
                gzip=False
                )
    
    return filename.replace('.csv.gz', '.csv')
                

def extract_green():
    context = get_current_context()
    data_start = context["data_interval_start"]
    year = data_start.year
    month = data_start.month

    # read csv
    filename = f'green_tripdata_{year}-{month:02}.csv.gz'
    url = f'{prefix}/download/green/{filename}'
    
    response = requests.get(url)
    response.raise_for_status()

    # decompress locally so bucket stores plain CSV
    with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as gz:
        decompressed_csv = gz.read()

    hook = GCSHook(gcp_conn_id='gcp-conn-id-1')
    bucket_name = BUCKET_NAME
    object_name = f"green/{filename.replace('.csv.gz', '.csv')}"
    print(object_name)
    hook.upload(bucket_name=bucket_name,
                object_name=object_name,
                mime_type='text/csv',
                data=decompressed_csv,
                gzip=False
                )
    
    return filename.replace('.csv.gz', '.csv')
    