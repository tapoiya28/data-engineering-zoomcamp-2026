with taxi_zone_lookup as (
    select * from "taxi_rides_ny"."dev"."taxi_zone_lookup"
), renamed as (
    select 
        cast(LocationID as integer) as location_id,
        Borough as borough,
        Zone as zone,
        service_zone
    from taxi_zone_lookup
)

select * from renamed