#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import argparse
import click
import pyarrow.parquet as pq

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
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

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]
@click.command()
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default='5431', help='PostgreSQL port')
@click.option('--db', default='ny_taxi', help='PostgreSQL database')
@click.option('--year', type=int, default=2021, help='Year for taxi data')
@click.option('--month', type=int, default=1, help='Month for taxi data')
@click.option('--table', default='yellow_taxi_data', help='Target table name')
@click.option('--chunksize', type=int, default=100000, help='Chunk size for reading CSV')

def run(user, password, host, port, db, year, month, table, chunksize):
    pg_user = user
    pg_password = password
    pg_host = host
    pg_port = port
    pg_db = db
    year = year
    month = month
    target_table = table + f"_{year}_{month:02d}"
    chunksize = chunksize

    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')
    
    #========ingest yellow taxi data
    # prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    # url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'

    # first = True
    # for df_chunk in tqdm(df_iters):
    #     if first:
    #         df_chunk.head(0).to_sql(
    #             name=target_table, 
    #             con=engine, 
    #             if_exists='replace'
    #         )
    #         first = False

    #     df_chunk.to_sql(
    #         name=target_table, 
    #         con=engine, 
    #         if_exists='append'
    #         )

    ##========ingest green taxi data
    # url_parquet = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
    # df_iters = pd.read_parquet(
    #     url_parquet
    # )

    # df_iters.to_sql(
    #     name=target_table,
    #     con=engine,
    #     if_exists='replace'
    # )

    ##========ingest taxi zone lookup data
    # url_zone = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'
    # df_zones = pd.read_csv(url_zone)
    # df_zones.to_sql(
    #     name='taxi_zones_lookup',
    #     con=engine,
    #     if_exists='replace'
    # )

if __name__ == '__main__':
    run()