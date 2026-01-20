from pytz import utc
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from datetime import datetime, timedelta
from ingest_taxi import extract_yellow, extract_green


default_args = {
    'owner': 'tapo',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='ny_taxi_v1-scheduled-ingest-v2',
    default_args=default_args,
    start_date=datetime(2019,1,1),
    schedule='0 9 1 * *',
    catchup=False,
) as dag:
    
    task_create_yellow_tables = SQLExecuteQueryOperator(
        task_id='create-yellow-tables',
        conn_id='ny_taxi_conn',
        sql="""
            CREATE TABLE IF NOT EXISTS yellow_taxi_data (
                unique_row_id          text,
                filename               text,
                VendorID               text,
                tpep_pickup_datetime   timestamp,
                tpep_dropoff_datetime  timestamp,
                passenger_count        integer,
                trip_distance          double precision,
                RatecodeID             text,
                store_and_fwd_flag     text,
                PULocationID           text,
                DOLocationID           text,
                payment_type           integer,
                fare_amount            double precision,
                extra                  double precision,
                mta_tax                double precision,
                tip_amount             double precision,
                tolls_amount           double precision,
                improvement_surcharge  double precision,
                total_amount           double precision,
                congestion_surcharge   double precision
            );
            CREATE TABLE IF NOT EXISTS yellow_taxi_data_staging (
                unique_row_id          text,
                filename               text,
                VendorID               text,
                tpep_pickup_datetime   timestamp,
                tpep_dropoff_datetime  timestamp,
                passenger_count        integer,
                trip_distance          double precision,
                RatecodeID             text,
                store_and_fwd_flag     text,
                PULocationID           text,
                DOLocationID           text,
                payment_type           integer,
                fare_amount            double precision,
                extra                  double precision,
                mta_tax                double precision,
                tip_amount             double precision,
                tolls_amount           double precision,
                improvement_surcharge  double precision,
                total_amount           double precision,
                congestion_surcharge   double precision
            );
        """,
        dag=dag
    )

    task_create_green_tables = SQLExecuteQueryOperator(
        task_id='create-green-tables',
        conn_id='ny_taxi_conn',
        sql="""
            CREATE TABLE IF NOT EXISTS green_taxi_data (
                unique_row_id          text,
                filename               text,
                VendorID               text,
                lpep_pickup_datetime   timestamp,
                lpep_dropoff_datetime  timestamp,
                store_and_fwd_flag     text,
                RatecodeID             text,
                PULocationID           text,
                DOLocationID           text,
                passenger_count        integer,
                trip_distance          double precision,
                fare_amount            double precision,
                extra                  double precision,
                mta_tax                double precision,
                tip_amount             double precision,
                tolls_amount           double precision,
                ehail_fee              double precision,
                improvement_surcharge  double precision,
                total_amount           double precision,
                payment_type           integer,
                trip_type              integer,
                congestion_surcharge   double precision
            );
            CREATE TABLE IF NOT EXISTS green_taxi_data_staging (
                unique_row_id          text,
                filename               text,
                VendorID               text,
                lpep_pickup_datetime   timestamp,
                lpep_dropoff_datetime  timestamp,
                store_and_fwd_flag     text,
                RatecodeID             text,
                PULocationID           text,
                DOLocationID           text,
                passenger_count        integer,
                trip_distance          double precision,
                fare_amount            double precision,
                extra                  double precision,
                mta_tax                double precision,
                tip_amount             double precision,
                tolls_amount           double precision,
                ehail_fee              double precision,
                improvement_surcharge  double precision,
                total_amount           double precision,
                payment_type           integer,
                trip_type              integer,
                congestion_surcharge   double precision
            );
        """,
        dag=dag
    )

    task_truncate_staging_yellow = SQLExecuteQueryOperator(
        task_id='truncate-staging-yellow',
        conn_id='ny_taxi_conn',
        sql="TRUNCATE TABLE yellow_taxi_data_staging;",
    )

    task_truncate_staging_green = SQLExecuteQueryOperator(
        task_id='truncate-staging-green',
        conn_id='ny_taxi_conn',
        sql="TRUNCATE TABLE green_taxi_data_staging;",
    )

    task_extract_load_staging_yellow = PythonOperator(
        task_id='extract-and-load-staging-yellow',
        python_callable=extract_yellow,
        dag=dag
    )

    task_extract_load_staging_green = PythonOperator(
        task_id='extract-and-load-staging-green',
        python_callable=extract_green,
        dag=dag
    )

    task_merge_yellow = SQLExecuteQueryOperator(
        task_id='merge-yellow',
        conn_id='ny_taxi_conn',
        sql="""
            MERGE INTO yellow_taxi_data AS T
            USING yellow_taxi_data_staging AS S
            ON T.unique_row_id = S.unique_row_id
            WHEN NOT MATCHED THEN 
            INSERT (
                unique_row_id, filename, VendorID, tpep_pickup_datetime, tpep_dropoff_datetime,
                passenger_count, trip_distance, RatecodeID, store_and_fwd_flag, PULocationID,
                DOLocationID, payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount,
                improvement_surcharge, total_amount, congestion_surcharge
            )
            VALUES (
                S.unique_row_id, S.filename, S.vendorid, S.tpep_pickup_datetime, S.tpep_dropoff_datetime,
                S.passenger_count, S.trip_distance, S.RatecodeID, S.store_and_fwd_flag, S.PULocationID,
                S.DOLocationID, S.payment_type, S.fare_amount, S.extra, S.mta_tax, S.tip_amount, S.tolls_amount,
                S.improvement_surcharge, S.total_amount, S.congestion_surcharge
            );
        """,
        dag=dag
    )

    task_merge_green = SQLExecuteQueryOperator(
        task_id='merge-green',
        conn_id='ny_taxi_conn',
        sql="""
            MERGE INTO green_taxi_data AS T
            USING green_taxi_data_staging AS S
            ON T.unique_row_id = S.unique_row_id
            WHEN NOT MATCHED THEN 
            INSERT (
                unique_row_id, filename, vendorid, lpep_pickup_datetime, lpep_dropoff_datetime,
                passenger_count, trip_distance, RatecodeID, store_and_fwd_flag, PULocationID,
                DOLocationID, payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount,
                improvement_surcharge, total_amount, congestion_surcharge, ehail_fee, trip_type
            )
            VALUES (
                S.unique_row_id, S.filename, S.vendorid, S.lpep_pickup_datetime, S.lpep_dropoff_datetime,
                S.passenger_count, S.trip_distance, S.RatecodeID, S.store_and_fwd_flag, S.PULocationID,
                S.DOLocationID, S.payment_type, S.fare_amount, S.extra, S.mta_tax, S.tip_amount, S.tolls_amount,
                S.improvement_surcharge, S.total_amount, S.congestion_surcharge, S.ehail_fee, S.trip_type
            );
        """,
        dag=dag
    )

    [task_create_yellow_tables >> task_truncate_staging_yellow >> task_extract_load_staging_yellow >> task_merge_yellow, 
     task_create_green_tables >> task_truncate_staging_green >> task_extract_load_staging_green >> task_merge_green] 
    # [task_merge_yellow, task_merge_green]