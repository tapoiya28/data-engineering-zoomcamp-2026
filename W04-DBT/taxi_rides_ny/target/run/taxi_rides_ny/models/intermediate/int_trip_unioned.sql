
  
  create view "taxi_rides_ny"."dev"."int_trip_unioned__dbt_tmp" as (
    with green_tripdata as (
    select * 
    from "taxi_rides_ny"."dev"."stg_green_tripdata"
)
, yellow_tripdata as (
    select *
    from "taxi_rides_ny"."dev"."stg_yellow_tripdata"
), trip_unioned as (
    select * from green_tripdata
    union all
    select * from yellow_tripdata
)

select * from trip_unioned
  );
