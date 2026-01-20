**Q1** \
692.6 MiB (624) \
**Q2** \
green_tripdata_2020-04.csv \
**Q3** 
```
select count(1) from yellow_taxi_data where filename like '%2020%';
```
29,430,127 ~ (28348499) \
**Q4** \
```
select count(1) from green_taxi_data where filename like '%2020%';
```
1,734,051 \
**Q5** \
```
select count(1) 
from yellow_taxi_data
where filename like '%2021-03%';
```
1,925,152 \
**Q6** \
Add a timezone property set to America/New_York in the Schedule trigger configuration
