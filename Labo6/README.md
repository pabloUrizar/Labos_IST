# LAB 6: DATA CATALOG AND PARQUET FILES
Authors : Valzino Benjamin, Urizar Pablo

## TASK 1: EXPLORE NEW YORK CITY TAXI TRIP DATA

**1) Navigate to the TLC Trip Record Data website. The taxi commission publishes data on four types of cabs. Which are
they?**

Yellow Taxi, Green Taxi, For-hire Vehicle, High Volume For-Hire Vehicle

**2) Find the PDF file with the data dictionary for the yellow cab data on web site. Does it contain the data types?**

The PDF with the data dictionary for the yellow cab data does not mention the data types for each field.
It contains information about the fields in the dataset along with their descriptions.

**3) The yellow cab data is available in what types of files?**

Starting from May 13, 2022, the yellow Taxi data is available in PARQUET format.

**4) Find the copy of the data product in the Registry of Open Data on AWS. What is the bucket name? In which region is
the bucket? Open the bucket in the S3 console.**

Bucket name : `nyc-tlc`
Region : `us-east-1`

![task1.png](screenshots%2Ftask1.png)

**5) In this lab we are going to use the yellow cab trip data. In which folder are the CSV files for yellow cabs? Does
this folder only contain yellow cab data? In which folder are the Parquet files for yellow cabs? Does this folder only
contain yellow cab data?**

CSV files for yellow cabs are in `s3://nyc-tlc/csv_backup/` folder. This folder contains data for all types of cabs.

CSV files for yellow cabs are also in `s3://nyc-tlc/opendata_repo/opendata_webconvert/yellow/` folder. This folder
contains data only for yellow cabs.

Parquet files for yellow cabs are in `s3://nyc-tlc/trip data/` folder. This folder contains data for all types of cabs.

## TASK 2: CREATE AN ENTRY IN THE DATA CATALOG AND QUERY THE DATA

**What subset of the data does the folder contain? In what format?**

The folder `aws-tc-largeobjects/CUR-TF-200-ACBDFO-1/Lab2/yellow/` contains a subset of New York City taxi trip data
for the year 2027 in CSV format. There is also a separate CSV file for each month.

**DDL definition of the table:**
```sql
CREATE EXTERNAL TABLE `yellow`(
  `vendorid` int, 
  `pickup` timestamp, 
  `dropoff` timestamp, 
  `passenger_count` float, 
  `trip_distance` float, 
  `ratecodeid` float, 
  `store_and_fwd_flag` string, 
  `pulocationid` int, 
  `dolocationid` int, 
  `payment_type` int, 
  `fare_amount` float, 
  `extra` float, 
  `mta_tax` float, 
  `tip_amount` float, 
  `tolls_amount` float, 
  `improvement_surcharge` float, 
  `total_amount` float, 
  `congestion_surcharge` float, 
  `airport_fee` float)
ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY ',' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://aws-tc-largeobjects/CUR-TF-200-ACBDFO-1/Lab2/yellow'
TBLPROPERTIES (
  'transient_lastDdlTime'='1702118016')
```

**6) Run a query that displays the first 10 records of the table:**
```sql
SELECT * FROM taxidata_grf.yellow
LIMIT 10;
```

**When the query completes, you will see a message "Completed - Time in queue: xxx ms Run time: yyy sec Data scanned:
zzz MB". Write down the run time and the volume of data scanned.**

Time in queue: 71 ms  
Run time: 1.965 sec  
Data scanned: 18.70 MB

**7) How much did the last query cost?**

Data Scanned (in TB) = 18.70 MB / 1024 = 0.0182 TB  
Cost = Data Scanned (in TB) * Price per TB  
Cost = 0.0182 TB * $5.00 = $0.091 USD  

The last query cost $0.091 USD.


## TASK 3: OPTIMISE THE QUERY BY SCANNING ONLY A PARTITION OF THE DATA

**1) Create a new table that contains just the data for January 2017 called jan, stored at
s3://aws-tc-largeobjects/CUR-TF-200-ACBDFO-1/Lab2/January2017/.**

**DDL definition of the table:**
```sql
CREATE EXTERNAL TABLE `jan`(
  `vendorid` int, 
  `pickup` timestamp, 
  `dropoff` timestamp, 
  `passenger_count` float, 
  `trip_distance` float, 
  `ratecodeid` float, 
  `store_and_fwd_flag` string, 
  `pulocationid` int, 
  `dolocationid` int, 
  `payment_type` int, 
  `fare_amount` float, 
  `extra` float, 
  `mta_tax` float, 
  `tip_amount` float, 
  `tolls_amount` float, 
  `improvement_surcharge` float, 
  `total_amount` float, 
  `congestion_surcharge` float, 
  `airport_fee` float)
ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY ',' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://aws-tc-largeobjects/CUR-TF-200-ACBDFO-1/Lab2/January2017'
TBLPROPERTIES (
  'transient_lastDdlTime'='1702122304')
```

**2) Run the following query on the data for the whole of 2017 that summarises trips in January 2017:**
```sql
SELECT  count(passenger_count) AS "Number of trips",
        sum(total_amount) AS "Total fares",
        pickup AS "Trip date"
FROM yellow WHERE pickup
between TIMESTAMP '2018-01-01 00:00:00'
     and TIMESTAMP '2018-02-01 00:00:01'
GROUP BY pickup;
```

Amount of data scanned: 9.32 GB

**3) Run the following query on the data for January 2017 only:**
```sql
SELECT count(passenger_count) AS "Number of trips" ,
        sum(total_amount) AS "Total fares" ,
        pickup AS "Trip date"
FROM jan
GROUP BY pickup;
```

Amount of data scanned: 815.30 MB

## TASK 4: CREATE A PARTITIONED TABLE IN THE DATA CATALOG WITH A GLUE CRAWLER

**DDL definition of the table:**
```sql
CREATE EXTERNAL TABLE `partyellow`(
  `vendorid` bigint, 
  `tpep_pickup_datetime` timestamp, 
  `tpep_dropoff_datetime` timestamp, 
  `passenger_count` double, 
  `trip_distance` double, 
  `ratecodeid` double, 
  `store_and_fwd_flag` string, 
  `pulocationid` bigint, 
  `dolocationid` bigint, 
  `payment_type` bigint, 
  `fare_amount` double, 
  `extra` double, 
  `mta_tax` double, 
  `tip_amount` double, 
  `tolls_amount` double, 
  `improvement_surcharge` double, 
  `total_amount` double, 
  `congestion_surcharge` double, 
  `airport_fee` double)
PARTITIONED BY ( 
  `year` string, 
  `month` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://heigvd-ist/nyc-tlc/yellow/'
TBLPROPERTIES (
  'CrawlerSchemaDeserializerVersion'='1.0', 
  'CrawlerSchemaSerializerVersion'='1.0', 
  'UPDATED_BY_CRAWLER'='nyc-tlc-grd', 
  'averageRecordSize'='26', 
  'classification'='parquet', 
  'compressionType'='none', 
  'objectCount'='45', 
  'partition_filtering.enabled'='true', 
  'recordCount'='169480265', 
  'sizeKey'='2552003645', 
  'typeOfData'='file')
```

**3) Examine the newly created table: On the left menu choose Databases. Select your NYC taxi trip database and locate
the newly created table. Click on it to view detailed information. View the schema. What virtual columns were added to
the schema? Also click on Partitions to view the partitions of the table.**

Virtual columns added to the schema: `year` and `month`

**4) In Athena write a query that makes use of the added virtual columns to restrict the scanning of data to August of
2022.** **How much data was scanned?**

```sql
SELECT *
FROM partyellow
WHERE year = '2022' AND month = '08';
```

Amount of data scanned: 47.40 MB


## TASK 5: EXPLORE AND TRANSFORM DATA WITH GLUE DATABREW

**2) Explore the statistics and visualisations DataBrew has generated for each column of the data. What is the largest
distance travelled (approximately)? What is the biggest tip given by a passenger (approximately)?**

![task5_3.png](screenshots%2Ftask5_3.png)

![task5_2.png](screenshots%2Ftask5_2.png)

**3) Verify the data types DataBrew has inferred from the data and correct them if necessary. Click on the Schema tab
to see an overview of the columns with their types. Click on the data type to change it.**

![task5_4.png](screenshots%2Ftask5_4.png)

**4) Write the data to a Parquet file in the bucket you created for the MeteoSwiss lab, How big are the generated
files?**

Schema of the generated Parquet files :

```sql
DESCRIBE taxidata_grd.parquet;
```

![task5_6.png](screenshots%2Ftask5_6.png)
