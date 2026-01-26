SELECT  
    dispatching_base_num,
    CAST(pickup_datetime as datetime) as pickup_datetime,
    CAST(dropOff_datetime as datetime) as dropoff_datetime,
    CAST(PULocationID as integer) as pu_location_id,
    CAST(DOLocationID as integer) as do_location_id,
    COALESCE(CAST(SR_Flag as integer), 0) as st_flag,
    Affiliated_base_number as affiliated_base_number
FROM {{ source('raw_data', 'fhv_tripdata') }} 
