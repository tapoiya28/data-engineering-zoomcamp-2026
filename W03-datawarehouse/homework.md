This homework use airflow to extract parquet files from source and load them into bucket. (DAG in folder airflow/) 

**Q1** 
```
SELECT count(*) FROM `dataengineer-zoomcamp-484202.ny_taxi.yellow_ext_parquet`
```
20,332,093 

**Q2** 
```
SELECT COUNT(DISTINCT(PULocationID))
FROM `dataengineer-zoomcamp-484202.ny_taxi.yellow_trip_data_mat`;
```
```
SELECT COUNT(DISTINCT(PULocationID))
FROM `dataengineer-zoomcamp-484202.ny_taxi.yellow_ext_parquet`;
```
0 MB for the External Table and 155.12 MB for the Materialized Table 

**Q3**
```
BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.
```

**Q4**
```
SELECT COUNT(*)
FROM `dataengineer-zoomcamp-484202.ny_taxi.yellow_trip_data_mat`
WHERE fare_amount = 0; 
```
8,333 

**Q5**

```
Partition by tpep_dropoff_datetime and Cluster on VendorID
```

**Q6**
```
SELECT DISTINCT(VendorID)
FROM `dataengineer-zoomcamp-484202.ny_taxi.yellow_trip_data_mat`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```
```
SELECT DISTINCT(VendorID)
FROM `dataengineer-zoomcamp-484202.ny_taxi.yellow_tripdata_mat_partitioned`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```
310.24 MB for non-partitioned table and 26.84 MB for the partitioned table 

**Q7** \
GCP Bucket 

**Q8** \
False 

**Q9** \
0B  
- Because bigquery store the metadata of table, including the number of rows of table. When estimate the query, GQ use the metadata instead of scanning the actual data.



