select 
    -- identifier
    CAST(VendorID AS INTEGER) as vendor_id,
    CAST(RatecodeID AS INTEGER) as rate_code_id,
    CAST(PULocationID AS INTEGER) as pu_location_id,
    CAST(DOLocationID AS INTEGER) as do_location_id,

    -- datetimme
    CAST(tpep_pickup_datetime AS DATETIME) as pickup_datetime,
    CAST(tpep_dropoff_datetime AS DATETIME) as dropoff_datetime,

    -- trip information
    store_and_fwd_flag,
    CAST(passenger_count AS INTEGER) as passenger_count,
    CAST(trip_distance AS NUMERIC) AS trip_distance,

    -- fee information
    CAST(fare_amount AS NUMERIC) as fare_amount,
    CAST(extra AS NUMERIC) as extra,
    CAST(mta_tax AS NUMERIC) as mta_tax,
    CAST(tip_amount AS NUMERIC) as tip_amount,
    CAST(tolls_amount AS NUMERIC) as tolls_amount,
    CAST(improvement_surcharge AS NUMERIC) as improvement_surcharge,
    CAST(total_amount AS NUMERIC) as total_amount,
    CAST(payment_type AS NUMERIC) as payment_type,
    CAST(congestion_surcharge AS NUMERIC) as congestion_surcharge

from "taxi_rides_ny"."prod"."yellow_tripdata"
where vendor_id not null