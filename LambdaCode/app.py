import logging
import json
import boto3
from io import BytesIO
import gzip

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def detect_http_flood(logfile):
    return ""
    # Loop through logfile
    # Create class object
    # Create list of class object
    # IP address = key, requests = value
    # if exists in list, add, if not, create new value


def parse_access_log_line(line):
    # Do something intelligent ... ?
    logger.info(line);

def decode_gzip(gzip_lines):
    gzip_file = BytesIO(gzip_lines)
    gzip_file = gzip.GzipFile(fileobj=gzip_file)
    decoded_zip = gzip_file.read()

    return decoded_zip

def retrieve_gzip_lines_from_bucket(event):

    # retrieve bucket name and file_key from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    logger.info('Reading {} from {}'.format(file_key, bucket_name))

    # get the object
    log_obj = s3.get_object(Bucket=bucket_name, Key=file_key)

    # get encoded gzip file
    gzip_lines = log_obj['Body'].read()

    return gzip_lines

def lambda_handler(event, context):

    logger.info("FLAG")
    logger.info(event)

    # Retrieve GZIP lines
    gzip_lines = retrieve_gzip_lines_from_bucket(event);

    # Decode gzipped access log file.
    decoded_access_log_file = decode_gzip(gzip_lines);

    logger.info(decoded_access_log_file)

    splitted_lines = decoded_access_log_file.split(b'\n')

    # Parse each line
    for line in splitted_lines:
        parse_access_log_line(line)
