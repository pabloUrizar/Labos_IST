# LAB 5: SERVERLESS DATA INGESTION AND PROCESSING
Authors : Valzino Benjamin, Urizar Pablo

## TASK 1: EXPLORE METEOSWISS DATA

**4. Explore the measurement values.**

**Data plausibility check: In the list of weather stations find one near you and write down its three-letter ID. In the
description of columns find the temperature column. In the measurement table look up the current temperature
measurement of the station. Does it correspond to what your thermometer or MeteoSwiss’ website or mobile app shows?**

Three-letter ID : PUY\
Current temperature measurement of station : 6.6 °C\
Météo Suisse : 6.4 °C

It is not exactly the same, but it is fairly accurate.

**In the measurement table examine the Date column (you may have to change its format to see it properly). What does it
contain exactly? Precision?**

The second column represents the timestamp in the format `YYYYMMDDHHmm` (Year, Month, Day, Hour, Minute).
In our case the timestamp for Pully is `202311181000` (2023-11-18 10:00). That means that the timestamp format provides
information down to the minute level. We tried to download it again after some time and the timestamp was
`202311181050` (2023-11-18 10:50). As stated in their website, we know that data is updated every 10 minutes.

**Delivrables :**\
<ins>URLs where the data can be downloaded</ins> :
- Automatic weather stations – Current measurement values : https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/data.zip \
- Weather stations of the automatic monitoring network : https://data.geo.admin.ch/ch.meteoschweiz.messnetz-automatisch/data.zip

<ins>Exploration of the measurement values</ins> :
- Automatic Weather Stations file : captures data from various weather stations in Switzerland, each reporting
measurements at ten-minute intervals. The file structure is organized with columns representing meteorological
parameters such as air temperature, precipitation, wind speed, and pressure, providing a comprehensive view of the
weather.
- Weather Stations Automatic Monitoring Network File : contains information about specific Swiss weather stations. The
file includes valuable details about each weather station such as its type, the date on which the data colluction began
and its altitude. It also displays meteorological parameters, including temperature, humidity, precipitation and even
radiation. Each station is also associated with a link where we can access supplementary information.

<ins>Impression of the opendata.swiss portal and of MeteoSwiss data products</ins> : the `opendata.swiss` portal is
great, it provides multiple datasets in a user-friendly manner. Navigating through the available information is
relatively straightforward. Another good point is that we can have access to accurate open data. `MeteoSwiss` products
are reliable and comprehensive, they deliver multiple meteorological insights that are easy to understand. The datasets
are well-organized and there is also a good documentation to help us in our exploration process. Overall, the
combination of a user-friendly portal and great meteorological datasets creates a good positive experience to open data
sources.

## TASK 2: UPLOAD THE CURRENT MEASUREMENT DATA TO S3 AND RUN SQL QUERIES ON IT

```sql
SELECT * FROM "meteoswiss_grd"."current" limit 10;
```

|  # | station | datetime      | temperature | precipitation | sunshine | radiation | humidity | despoint | wind_dir | wind_speed | gust_peak | pressure | press_sea | press_sea_qnh | height_850_hpa | heigh_700_hpa | wind_dir_vec | wind_speed_tower | gust_peak_tower | temp_tool1 | humidity_tower | dew_point_tower |
|---|---------|---------------|-------------|---------------|----------|-----------|----------|----------|----------|------------|-----------|----------|-----------|---------------|-----------------|----------------|--------------|-------------------|-----------------|------------|-----------------|------------------|
| 1 | TAE     | 202311240930  | 6.6         | 0.0           | 0.0      | 136.0     | 83.0     | 3.9      | 219.0    | 17.6       | 36.7      | 950.4    | 1014.5    | 1013.6        |                 |                |              |                   |                 |            |                 |                  |
| 2 | COM     | 202311240930  | 17.5        | 0.0           | 10.0     | 361.0     | 18.4     | -6.8     | 357.0    | 23.8       | 40.3      | 940.2    | 1005.3    | 1007.2        |                 |                |              |                   |                 |            |                 |                  |
| 3 | ABO     | 202311240930  | 0.6         | 0.0           | 10.0     | 318.0     | 80.6     | -2.3     | 89.0     | 5.4        | 9.7       | 865.5    |           | 1015.2        | 1470.8          |                |              |                   |                 |            |                 |                  |
| 4 | AIG     | 202311240930  | 4.8         | 0.0           | 0.0      | 47.0      | 84.9     | 2.5      | 354.0    | 1.1        | 2.2       | 973.3    | 1019.8    | 1018.6        |                 |                |              |                   |                 |            |                 |                  |
| 5 | ALT     | 202311240930  | 4.0         | 0.0           | 1.0      | 162.0     | 82.5     | 1.3      | 143.0    | 2.5        | 5.4       | 964.3    | 1017.6    | 1016.1        |                 |                |              |                   |                 |            |                 |                  |
| 6 | ARH     | 202311240930  | 10.5        | 0.0           | 8.0      | 348.0     | 63.1     | 3.8      | 228.0    | 26.6       | 58.7      | 965.2    | 1012.3    | 1012.1        |                 |                |              |                   |                 |            |                 |                  |
| 7 | AND     | 202311240930  | -2.3        | 0.0           | 5.0      | 96.0      | 85.9     | -4.3     | 82.0     | 2.2        | 5.4       | 900.0    |           | 1013.2        | 1439.9          |                |              |                   |                 |            |                 |                  |
| 8 | ANT     | 202311240930  | -1.3        | 0.0           | 6.0      | 116.0     | 84.0     | -3.6     | 86.0     | 5.4        | 15.1      | 852.5    |           | 1013.5        | 1459.1          |                |              |                   |                 |            |                 |                  |
| 9 | ARO     | 202311240930  | -0.6        | 0.0           | 0.0      | 124.0     | 72.0     | -5.0     | 91.0     | 3.2        | 7.9       | 805.5    |           | 1011.5        | 1446.4          |                |              |                   |                 |            |                 |                  |
|10 | RAG     | 202311240930  | 4.1         | 0.0           | 0.0      | 173.0     | 78.5     | 0.7      | 133.0    | 12.2       | 18.4      | 956.3    | 1016.2    | 1014.7        |                 |                |              |                   |                 |            |                 |                  |


## TASK 3: WRITE A PYTHON SCRIPT TO DOWNLOAD THE CURRENT MEASUREMENT VALUES FROM METEOSWISS AND UPLOAD THEM TO S3

lambda_function.py :
```python
import json
import requests
import logging
import boto3
from botocore.exceptions import ClientError

def upload_file(content, bucket, object_name):
    # Upload the file
    s3_client = boto3.client('s3')

    try:
        s3_client.put_object(Body=content, Bucket=bucket, Key=object_name)
        logging.info(f"File uploaded to S3: {object_name}")
        return True
    except ClientError as e:
        logging.error(f"Failed to upload file to S3: {e}")
        return False

def lambda_handler(event, context):
    logging.info("Function invoked with event %s", json.dumps(event))

    response = requests.get('https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/VQHA80.csv')

    if upload_file(response.content, "ist-meteo-grd-urizar-valzino", "current/data-meteo.csv"):
        return {
            'statusCode': 200,
            'body': json.dumps('File Uploaded Successfully!')
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to upload file to S3')
        }
```

local_test.py :
```python
import json
from lambda_function import lambda_handler

# Simulate an event, you can adjust this based on your actual event structure
sample_event = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
}

# Call the Lambda handler function
result = lambda_handler(sample_event, None)

# Print the result (you can customize this based on your expected return format)
print(json.dumps(result, indent=2))
```

Test :
```shell
pablo@Macbook-Pro-M1 Labo5 % python3 local_test.py 
{
  "statusCode": 200,
  "body": "\"File Uploaded Successfully!\""
}
```

## TASK 4: CONVERT YOUR SCRIPT INTO AN AWS LAMBDA FUNCTION FOR DATA INGESTION

lambda_function.py :
```python
import json
import requests
import logging
import boto3
from botocore.exceptions import ClientError
import datetime

def upload_file(content, bucket, object_name):
    # Upload the file
    s3_client = boto3.client('s3')

    try:
        s3_client.put_object(Body=content, Bucket=bucket, Key=object_name)
        logging.info(f"File uploaded to S3: {object_name}")
        return True
    except ClientError as e:
        logging.error(f"Failed to upload file to S3: {e}")
        return False

def lambda_handler(event, context):
    logging.info("Function invoked with event %s", json.dumps(event))

    # Generate the object name with the desired naming convention
    datetimenow = datetime.datetime.now().replace(microsecond=0).strftime("%Y-%m-%dT%H:%M")
    object_name = f"current/VQHA80-{datetimenow}.csv"

    response = requests.get('https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/VQHA80.csv')

    if upload_file(response.content, "ist-meteo-grd-urizar-valzino", object_name):
        return {
            'statusCode': 200,
            'body': json.dumps('File Uploaded Successfully!')
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to upload file to S3')
        }
```

Customer managed policy `writeAccess-grd` attached to the role `meteoswiss-ingest-grd-role-753jbau6` :
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::ist-meteo-grd-urizar-valzino/*"
            ],
            "Effect": "Allow"
        }
    ]
}
```

## TASK 5: CREATE AN EVENT RULE THAT TRIGGERS YOUR FUNCTION EVERY 10 MINUTES

## TASK 6: TRANSFORM THE WEATHER STATIONS FILE INTO A CSV FILE

**4. Examine the YAML. There are two top-level keys, what are their names?**

We found the following top-level keys :
```shell
$ cat file.json | jq -r 'keys[]'
creation_time
crs
features
license
map_abstract
map_long_name
map_short_name
mapname
type
```

Key that has an array as value :
```shell
$ cat file.json | jq -r 'to_entries[] | select(.value | type == "array") | .key'
features
```

Final jq command :
```shell
jq -r '         
  ["id", "station_name", "altitude", "coord_lng", "coord_lat"],
  (.features[] | [
    .id,
    "\"\(.properties.station_name)\"",
    (.properties.altitude | tostring),
    (.geometry.coordinates[0] | tostring),
    (.geometry.coordinates[1] | tostring)
  ])
  | join(",")
' file.json > stations.csv
```

## TASK 7: QUERY THE ACCUMULATED DATA

**1. Inspect your current folder and remove any duplicates that remain from testing. It should contain several
measurement files, each with a distinct timestamp in the filename.**

```shell
aws s3 ls s3://ist-meteo-grd-urizar-valzino/current/ --recursive | awk '{print $4}' | sort | uniq -d
```

No objects were displayed so we do not have any duplicates.

**2. Using Amazon Athena, make a query that returns all measurements for the Payerne station (PAY), sorted by ascending
datetime.**

```sql
SELECT *
FROM meteoswiss_grd.current
WHERE station = 'PAY'
ORDER BY datetime ASC
limit 10;
```

| #   | station | datetime        | temperature | precipitation | sunshine | radiation |
|-----|---------|-----------------|-------------|---------------|----------|-----------|
| 1   | PAY     | 202311181000    | 4.7         | 0.0           | 0.0      | 131.0     |
| 2   | PAY     | 202311201620    | 9.9         | 0.0           | 0.0      | 0.0       |
| 3   | PAY     | 202311201630    | 9.8         | 0.0           | 0.0      | 0.0       |
| 4   | PAY     | 202311201640    | 9.7         | 0.0           | 0.0      | 0.0       |
| 5   | PAY     | 202311201650    | 9.7         | 0.0           | 0.0      | 0.0       |
| 6   | PAY     | 202311201700    | 9.6         | 0.0           | 0.0      | 0.0       |
| 7   | PAY     | 202311201710    | 9.3         | 0.0           | 0.0      | 0.0       |
| 8   | PAY     | 202311201720    | 9.3         | 0.0           | 0.0      | 0.0       |
| 9   | PAY     | 202311201730    | 9.1         | 0.0           | 0.0      | 0.0       |
| 10  | PAY     | 202311201740    | 9.2         | 0.0           | 0.0      | 0.0       |

**3. For Payerne, make a query that returns the maximum temperature for each hour, sorted by increasing hour.**

```sql
SELECT
    date_trunc('hour', date_parse(CAST(datetime AS VARCHAR), '%Y%m%d%H%i')) AS hour,
  MAX(temperature) AS max_temperature
FROM meteoswiss_grd.current
WHERE station = 'PAY'
GROUP BY date_trunc('hour', date_parse(CAST(datetime AS VARCHAR), '%Y%m%d%H%i'))
ORDER BY hour
limit 10;
```

| #   | hour                         | max_temperature |
|-----|------------------------------|-----------------|
| 1   | 2023-11-18 10:00:00.000      | 4.7             |
| 2   | 2023-11-20 16:00:00.000      | 9.9             |
| 3   | 2023-11-20 17:00:00.000      | 9.6             |
| 4   | 2023-11-20 18:00:00.000      | 9.3             |
| 5   | 2023-11-20 19:00:00.000      | 9.4             |
| 6   | 2023-11-20 20:00:00.000      | 8.6             |
| 7   | 2023-11-20 21:00:00.000      | 8.0             |
| 8   | 2023-11-20 22:00:00.000      | 7.6             |
| 9   | 2023-11-20 23:00:00.000      | 7.4             |
| 10  | 2023-11-21 00:00:00.000      | 7.3             |


**4. Create a table for the stations folder. Find all stations whose altitude is similar to Yverdon, i.e. 400 m
<= altitude < 500 m, sorted by altitude.**

```sql
SELECT *
FROM meteoswiss_grd.stations
WHERE altitude >= 400 AND altitude < 500
ORDER BY altitude
limit 10;
```

| id | station | station_name         | altitude | coord_lng | coord_lat |
|----|---------|----------------------|----------|---------|---------|
| 1  | BEX     | "Bex"                | 402.0    | 2565805 | 1121511 |
| 2  | BUE     | "Bülach"             | 403.0    | 2682029 | 1263775 |
| 3  | VEV     | "Vevey / Corseaux"   | 405.0    | 2552106 | 1146847 |
| 4  | SCM     | "Schmerikon"         | 408.0    | 2713726 | 1231533 |
| 5  | DOB     | "Benken / Doggen"    | 408.0    | 2715388 | 1227540 |
| 6  | OBR     | "Oberriet / Kriesser"| 409.0    | 2764171 | 1249582 |
| 7  | JON     | "Jona"               | 410.0    | 2706761 | 1231290 |
| 8  | GVE     | "Genève / Cointrin"  | 411.0    | 2498904 | 1122632 |
| 9  | ESZ     | "Eschenz"            | 414.0    | 2707844 | 1278214 |
| 10 | CEV     | "Cevio"              | 417.0    | 2689688 | 1130564 |

**5. Find the maximum temperature of all stations at an altitude similar to Yverdon, sorted by altitude.**

```sql
SELECT
  s.id,
  s.station_name,
  s.altitude,
  MAX(c.temperature) AS max_temperature
FROM
  meteoswiss_grd.stations s
JOIN
  meteoswiss_grd.current c
ON
  s.id = c.station
WHERE
  s.altitude >= 400 AND s.altitude < 500
GROUP BY
  s.id, s.station_name, s.altitude
ORDER BY
  s.altitude;
```

| id  | station_name           | altitude | max_temperature |
|-----|------------------------|----------|-----------------|
| 1   | VEV                    | "Vevey / Corseaux"        | 405.0    | 11.7            |
| 2   | SCM                    | "Schmerikon"              | 408.0    |                  |
| 3   | OBR                    | "Oberriet / Kriesser"     | 409.0    | 10.3            |
| 4   | GVE                    | "Genève / Cointrin"       | 411.0    | 11.4            |
| 5   | CEV                    | "Cevio"                   | 417.0    | 21.2            |
| 6   | HLL                    | "Hallau"                  | 419.0    | 9.8             |
| 7   | QUI                    | "Quinten"                 | 419.0    |                  |
| 8   | WYN                    | "Wynau"                   | 422.0    | 8.6             |
| 9   | PRE                    | "St-Prex"                 | 425.0    |                  |
| 10  | KLO                    | "Zürich / Kloten"         | 426.0    | 9.6             |
| 11  | GRE                    | "Grenchen"                | 428.0    | 10.5            |
| 12  | CRM                    | "Cressier"                | 430.0    | 11.0            |
| 13  | MAH                    | "Mathod"                  | 435.0    | 10.7            |
| 14  | ALT                    | "Altdorf"                 | 438.0    | 9.8             |
| 15  | SHA                    | "Schaffhausen"            | 438.0    | 9.6             |
| 16  | DEM                    | "Delémont"                | 439.0    | 9.8             |
| 17  | GUT                    | "Güttingen"               | 440.0    | 10.0            |
| 18  | CHZ                    | "Cham"                    | 443.0    | 11.0            |
| 19  | REH                    | "Zürich / Affoltern"      | 444.0    | 9.7             |
| 20  | MOA                    | "Mosen"                   | 453.0    | 10.9            |
| 21  | LUZ                    | "Luzern"                  | 454.0    | 12.6            |
| 22  | PUY                    | "Pully"                   | 456.0    | 10.8            |
| 23  | VAD                    | "Vaduz"                   | 457.0    | 12.0            |
| 24  | CGI                    | "Nyon / Changins"         | 458.0    | 11.0            |
| 25  | LAC                    | "Lachen / Galgenen"       | 468.0    | 11.3            |
| 26  | GIH                    | "Giswil"                  | 471.0    | 11.8            |
| 27  | MUB                    | "Mühleberg"               | 480.0    | 10.3            |
| 28  | SIO                    | "Sion"                    | 482.0    | 10.9            |
| 29  | EVI                    | "Evionnaz"                | 482.0    | 10.8            |
| 30  | NEU                    | "Neuchâtel"               | 485.0    | 10.4            |
| 31  | WAE                    | "Wädenswil"               | 485.0    | 10.8            |
| 32  | KOP                    | "Koppigen"                | 485.0    | 9.5             |
| 33  | PAY                    | "Payerne"                 | 490.0    | 10.1            |
| 34  | STC                    | "St. Chrischona"          | 493.0    |                  |
| 35  | RAG                    | "Bad Ragaz"               | 497.0    | 10.8            |


## TASK 8: WRITE AN S3 OBJECT LAMBDA FUNCTION TO TRANSFORM DATA

lambda_function.py :
```python
import csv
import boto3
from datetime import datetime

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Extract bucket and key from the event
    bucket = event['bucket']
    key = event['key']

    # Fetch the specified object
    object_content = s3.get_object(Bucket=bucket, Key=key)['Body'].read().decode('utf-8')

    # Process the data
    processed_data = process_data(object_content)

    # Define the output key in the 'pretty/' folder
    output_key = f"pretty/{key.split('/')[-1]}"

    # Upload the processed data to S3
    s3.put_object(Body=processed_data, Bucket=bucket, Key=output_key)

def process_data(data):
    rows = [row.split(';') for row in data.split('\n')]
    header = rows[0]
    rename = [
        'station', 'year', 'month', 'day', 'hour', 'minute',
        'temperature', 'precipitation', 'sunshine',
        'radiation', 'humidity', 'despoint', 'wind_dir', 'wind_speed',
        'gust_peak', 'pressure', 'press_sea', 'press_sea_qnh',
        'height_850_hpa', 'heigh_700_hpa', 'wind_dir_vec',
        'wind_speed_tower', 'gust_peak_tower', 'temp_tool1',
        'humidity_tower', 'dew_point_tower'
    ]

    header = [rename[i] for i in range(len(rename))]
    output_rows = [header]
    
    for i, row in enumerate(rows[1:], start=1):
        if len(row) >= 2:
            try:
                string_date = row[1]
                year = string_date[:4]
                month = string_date[4:6]
                day = string_date[6:8]
                hour = string_date[8:10]
                minute = string_date[10:12]
                new_row = [row[0]] + [year, month, day, hour, minute] + row[2:]
                output_rows.append(new_row)
            except Exception as e:
                print(f"Error processing row {i}: {e}")
                print(f"Row content: {row}")

    output_csv = '\n'.join([','.join(map(str, row)) for row in output_rows])

    return output_csv
```

Event JSON :
```json
{
  "bucket": "ist-meteo-grd-urizar-valzino",
  "key": "current/VQHA80-2023-11-20T16:31.csv"
}
```