
  
  create view "taxi_rides_ny"."dev"."dim_vendor__dbt_tmp" as (
    with trip_unioned as (
    select * from "taxi_rides_ny"."dev"."int_trip_unioned"
)

select * from trip_unioned
  );
