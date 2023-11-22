# LAB 5: SERVERLESS DATA INGESTION AND PROCESSING
Authors : Valzino Benjamin, Urizar Pablo

### TASK 1: EXPLORE METEOSWISS DATA

**4. Explore the measurement values.**

*Data plausibility check: In the list of weather stations find one near you and write down its three-letter ID. In the
description of columns find the temperature column. In the measurement table look up the current temperature
measurement of the station. Does it correspond to what your thermometer or MeteoSwiss’ website or mobile app shows?*

Three-letter ID : PUY\
Current temperature measurement of station : 6.6 °C\
Météo Suisse : 6.4 °C

It is not exactly the same, but it is fairly accurate.

*In the measurement table examine the Date column (you may have to change its format to see it properly). What does it
contain exactly? Precision?*

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

### TASK 2: UPLOAD THE CURRENT MEASUREMENT DATA TO S3 AND RUN SQL QUERIES ON IT

### TASK 3: WRITE A PYTHON SCRIPT TO DOWNLOAD THE CURRENT MEASUREMENT VALUES FROM METEOSWISS AND UPLOAD THEM TO S3

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

### TASK 4: CONVERT YOUR SCRIPT INTO AN AWS LAMBDA FUNCTION FOR DATA INGESTION

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

### TASK 5: CREATE AN EVENT RULE THAT TRIGGERS YOUR FUNCTION EVERY 10 MINUTES

### TASK 6: TRANSFORM THE WEATHER STATIONS FILE INTO A CSV FILE

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
echo "id,station_name,altitude,coord_lng,coord_lat" > output.csv && \
cat file.json | jq -r '.features[] | [.id, .properties.station_name, .properties.altitude, .geometry.coordinates[0], .geometry.coordinates[1]] | @csv' >> output.csv
```