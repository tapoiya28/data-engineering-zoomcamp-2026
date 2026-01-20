import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import hashlib

from airflow.sdk import get_current_context

prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases'

dtype_yellow = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PUlocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates_yellow = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

dtype_green = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PUlocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "trip_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "ehail_fee": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
}

parse_dates_green = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime"
]

table_yellow = 'yellow_taxi_data'
staging_table_yellow = f'{table_yellow}_staging'
table_green = 'green_taxi_data'
staging_table_green = f'{table_green}_staging'

def extract_yellow():
    context = get_current_context()

    data_start = context["data_interval_start"]

    year = data_start.year
    month = data_start.month

    # read csv
    url = f'{prefix}/download/yellow/yellow_tripdata_{year}-{month:02}.csv.gz'
    print(url)
    df_iter = pd.read_csv(
        url,
        dtype=dtype_yellow,
        parse_dates=parse_dates_yellow,
        iterator=True,
        chunksize=100000
        )
    
    # create db engine
    engine = create_engine('postgresql://root:root@pgdatabase:5432/ny_taxi')

    for df_chunk in df_iter:
        df_chunk.columns = df_chunk.columns.str.lower()
        # add extra columns
        df_chunk.insert(0, 'unique_row_id', None)
        df_chunk.insert(1, 'filename', f'yellow_tripdata_{year}-{month:02}.csv')
        
        hash_cols = [
            "vendorid",
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "trip_distance",
            "pulocationid",
            "dolocationid",
            "fare_amount",
        ]    
        
        hash_df = df_chunk[hash_cols].astype(str).fillna('')
        concat = hash_df.agg(''.join, axis=1)
        df_chunk["unique_row_id"] = concat.apply(lambda row: hashlib.md5(row.encode()).hexdigest())
        
        df_chunk.to_sql(name=staging_table_yellow, con=engine, if_exists='append', index=False)

def extract_green():
    context = get_current_context()
    data_start = context["data_interval_start"]

    year = data_start.year
    month = data_start.month
    
    # read csv
    url = f'{prefix}/download/green/green_tripdata_{year}-{month:02}.csv.gz'
    print(url)
    df_iter = pd.read_csv(
        url,
        dtype=dtype_green,
        parse_dates=parse_dates_green,
        iterator=True,
        chunksize=100000
        )
    
    # create db engine
    engine = create_engine('postgresql://root:root@pgdatabase:5432/ny_taxi')

    for df_chunk in df_iter:
        # add extra columns
        df_chunk.columns = df_chunk.columns.str.lower()
        df_chunk.insert(0, 'unique_row_id', None)
        df_chunk.insert(1, 'filename', f'green_tripdata_{year}-{month:02}.csv')

        hash_cols = [
            "vendorid",
            "lpep_pickup_datetime",
            "lpep_dropoff_datetime",
            "trip_distance",
            "pulocationid",
            "dolocationid",
            "fare_amount",
        ]    
        
        hash_df = df_chunk[hash_cols].astype(str).fillna('')
        concat = hash_df.agg(''.join, axis=1)
        df_chunk["unique_row_id"] = concat.apply(lambda row: hashlib.md5(row.encode()).hexdigest())

        print(df_chunk.columns.tolist())
        
        df_chunk.to_sql(name=staging_table_green, con=engine, if_exists='append', index=False)