

with green_taxi as (
    select 
        vendor_id,
        rate_code_id,
        pu_location_id,
        do_location_id,
        -- datetimme
        pickup_datetime,
        dropoff_datetime,
        -- trip information
        store_and_fwd_flag,
        passenger_count,
        trip_type,
        trip_distance,
        -- fee information
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        ehail_fee,
        improvement_surcharge,
        total_amount,
        payment_type,
        'green' as service_type
    from "taxi_rides_ny"."dev"."stg_green_tripdata"
), yellow_taxi as (
    select 
        vendor_id,
        rate_code_id,
        pu_location_id,
        do_location_id,
        -- datetimme
        pickup_datetime,
        dropoff_datetime,
        -- trip information
        store_and_fwd_flag,
        passenger_count,
        1 as trip_type,
        trip_distance,
        -- fee information
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        0 as ehail_fee,
        improvement_surcharge,
        total_amount,
        payment_type,
        'yellow' as service_type
    from "taxi_rides_ny"."dev"."stg_yellow_tripdata"
), trip_unioned as (
    select * from yellow_taxi
    union all
    select * from green_taxi
)

select * from trip_unioned