with trip_unioned as (
    select *
    from {{ref('int_trip_unioned')}}
), vendors as (
    select 
        distinct vendor_id
    from trip_unioned
)

select
    vendor_id,
    {{ get_vendor_data('vendor_id') }}
from vendors