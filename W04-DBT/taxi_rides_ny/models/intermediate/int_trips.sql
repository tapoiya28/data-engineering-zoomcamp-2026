with unioned as (
    select * from {{ ref('int_trip_unioned') }}
), cleaned_and_enriched as (

    select 
        -- Identifiers
        u.vendor_id,
        u.rate_code_id,

        -- Location IDs
        u.pickup_location_id,
        u.dropoff_location_id,

        -- Timestamps
        u.pickup_datetime,
        u.dropoff_datetime,

        -- Trip details
        u.store_and_fwd_flag,
        u.passenger_count,
        u.trip_distance,
        u.trip_type,

        -- Payment breakdown
        u.fare_amount,
        u.extra,
        u.mta_tax,
        u.tip_amount,
        u.tolls_amount,
        u.ehail_fee,
        u.improvement_surcharge,
        u.total_amount,

        -- Enrich with payment type description
        coalesce(u.payment_type, 0) as payment_type,
    from unioned u
)
select * from cleaned_and_enriched

qualify row_number() over(
    partition by vendor_id, pickup_datetime, pickup_location_id
    order by dropoff_datetime
) = 1
