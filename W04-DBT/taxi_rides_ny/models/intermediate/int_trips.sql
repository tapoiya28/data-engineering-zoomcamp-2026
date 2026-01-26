with trip_unioned as (
    select *
    from {{ ref('int_trip_unioned') }}    
), payment_type as (
    select * 
    from {{ ref('payment_type_lookup') }}
), cleaned_and_enrich as (
    select 

        -- add primary key
        {{ dbt_utils.generate_surrogate_key(
            ['trip.vendor_id', 'trip.pickup_datetime', 'trip.pu_location_id', 'trip.service_type']
            ) 
        }} as trip_id, 

        -- identifier
        trip.vendor_id,
        trip.rate_code_id,
        trip.service_type,
        -- location id
        trip.pu_location_id,
        trip.do_location_id,
        -- datetimme
        trip.pickup_datetime,
        trip.dropoff_datetime,
        -- trip information
        trip.store_and_fwd_flag,
        trip.passenger_count,
        trip.trip_type,
        trip.trip_distance,
        -- fee information
        trip.fare_amount,
        trip.extra,
        trip.mta_tax,
        trip.tip_amount,
        trip.tolls_amount,
        trip.ehail_fee,
        trip.improvement_surcharge,
        trip.total_amount,
        
        coalesce(trip.payment_type, 0) as payment_type,
        coalesce(payment.description, 'Unknown') as payment_type_description 


    from trip_unioned trip 
    left join payment_type payment ON trip.payment_type = payment.payment_type
)

select * from cleaned_and_enrich
qualify row_number() over (
    partition by vendor_id, pickup_datetime, pu_location_id, service_type
    order by dropoff_datetime
) = 1