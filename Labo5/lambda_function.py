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
