**Q1**
  docker run -it --entrypoint bash python:3.13
  >> pip --version

**Q2**
db:5432

-- SQL
**Q3**
```
select count(*)
from public."green_trip_data_2025_11"
where "trip_distance" <= 1.0
	and "lpep_pickup_datetime" < '2025-12-01';
```

**Q4**
```
select 
	"lpep_pickup_datetime"
from public."green_trip_data_2025_11"
where "trip_distance" < 100
order by trip_distance desc;
```

**Q5**
```
select 
	z."LocationID",
	z."Zone",
	sum(t."total_amount") as largest_amount
from public."green_trip_data_2025_11" as t
join public."taxi_zones_lookup" as z on t."PULocationID" = z."LocationID"
where t."lpep_pickup_datetime" > '2025-11-17' and t."lpep_pickup_datetime" < '2025-11-19'
group by z."LocationID", z."Zone"
order by largest_amount desc;
```

**Q6**
```
select 
	zdo."LocationID",
	zdo."Zone",
	max(t."tip_amount") as largest_tip
from public."green_trip_data_2025_11" as t
join public."taxi_zones_lookup" as zpu on t."PULocationID" = zpu."LocationID"
join public."taxi_zones_lookup" as zdo on t."DOLocationID" = zdo."LocationID"
where zpu."Zone" = 'East Harlem North'
group by zdo."LocationID", zdo."Zone"
order by largest_tip desc;
```

**Q7**
terraform init, terraform apply -auto-approve, terraform destroy
