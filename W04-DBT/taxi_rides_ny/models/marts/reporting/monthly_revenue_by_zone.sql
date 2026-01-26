SELECT 
    -- group zone
    coalesce(pu_zone, 'Unknown zone') as pickup_zone,
    date_trunc('month', pickup_datetime) as revenuez_month,
    service_type,

    -- revenue breakdown
    sum(fare_amount) as revenue_monthly_fare,
    sum(extra) as revenue_monthly_extra,
    sum(mta_tax) as revenue_monthly_mta_tax,
    sum(tip_amount) as revenue_monthly_tip_amount,
    sum(tolls_amount) as revenue_monthly_tolls_amount,
    sum(ehail_fee) as revenue_monthly_ehail_fee,
    sum(improvement_surcharge) as revenue_monthly_improvement_surcharge,
    sum(total_amount) as revenue_monthly_total_amount,

    -- additional metrics
    count(trip_id) as total_monthly_trips,
    avg(passenger_count) as total_monthly_passengers
    avg(trip_distance) as total_monthly_trip_distances

FROM {{ ref('fct_trips') }}
GROUP BY pu_zone, date_trunc, service_type