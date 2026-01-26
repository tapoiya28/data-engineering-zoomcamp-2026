{{
  config(
    materialized='incremental',
    unique_key='trip_id',
    on_schema_change='fail'
  )
}}

select 
  -- trip identifier
  trip.trip_id,
  trip.vendor_id,
  trip.service_type,
  trip.rate_code_id,

  -- location detail
  trip.pu_location_id,
  pz.borough as pu_borough,
  pz.zone as pu_zone,
  trip.do_location_id,
  dz.borough as do_borough,
  dz.zone as do_zone,

  -- trip timing
  trip.pickup_datetime,
  trip.dropoff_datetime,
  trip.store_and_fwd_flag,

  -- trip metrics
  trip.passenger_count,
  trip.trip_distance,
  trip.trip_type,

  -- payment
  trip.fare_amount,
  trip.extra,
  trip.mta_tax,
  trip.tip_amount,
  trip.tolls_amount,
  trip.ehail_fee,
  trip.improvement_surcharge,
  trip.total_amount,
  trip.payment_type,
  trip.payment_type_description
  
from {{ ref('int_trips') }} as trip
left join {{ ref('dim_zones') }} as pz
  on trip.pu_location_id = pz.location_id
left join {{ ref('dim_zones') }} as dz
  on trip.do_location_id = dz.location_id

{% if is_incremental() %}
  -- Only process new trips based on pickup datetime
  where trip.pickup_datetime > (select max(pickup_datetime) from {{ this }})
{% endif %}
