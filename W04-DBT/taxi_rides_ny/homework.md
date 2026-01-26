## Q1
- Any model with upstream and downstream dependencies to int_trips_unioned
## Q2
- dbt will fail the test, returning a non-zero exit code
## Q3
```
select count(*) from {{ ref('monthly_revenue_by_zone') }}
```
- 12,184

## Q4
```
select  
    pickup_zone,
    sum(revenue_monthly_total_amount) as total_amount_zone
from from {{ ref('monthly_revenue_by_zone') }}
where service_type = 'green'
    and revenue_month between '2020-01-01' and '2020-12-31'
group by pickup_zone
order by total_amount_zone desc
```

- East Harlem North

## Q5
```
select  
    sum(total_monthly_trips) as total_trips
from from {{ ref('monthly_revenue_by_zone') }}
where service_type = 'green'
    and revenue_month between '2019-10-01' and '2019-10-30'
```
- 384,624
## Q6
```
SELECT  
    dispatching_base_num,
    CAST(pickup_datetime as datetime) as pickup_datetime,
    CAST(dropOff_datetime as datetime) as dropoff_datetime,
    CAST(PULocationID as integer) as pu_location_id,
    CAST(DOLocationID as integer) as do_location_id,
    COALESCE(CAST(SR_Flag as integer), 0) as st_flag,
    Affiliated_base_number as affiliated_base_number
FROM {{ source('raw_data', 'fhv_tripdata') }} 
```
```
select count(*) 
from {{ ref('stg_fhv_tripdata') }}
```
- 43,244,696