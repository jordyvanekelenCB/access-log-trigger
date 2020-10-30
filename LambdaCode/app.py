import logging
import boto3
from helper import AWSS3
from helper import ALBLogParser

# Setup boto3 session
session = boto3.Session()

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create boto3 s3 client
s3 = boto3.client('s3')


def detect_http_flood(logfile_object):

    return ""
    # Loop through logfile
    # Create class object
    # Create list of class object
    # IP address = key, requests = value
    # if exists in list, add, if not, create new value

    # TODO: DAAN, mentor verwerken (meerdere lambda in 1 project) clean architecture



def lambda_handler(event, context):

    # Instantiate aws s3 helper
    awss3_helper = AWSS3(event, s3)
    alb_log_parser_helper = ALBLogParser()

    # Retrieve alb log file
    alb_log_file = awss3_helper.getAWSLogFile()

    # Parse alb log file into array of objects
    alb_log_array = alb_log_parser_helper.parse_alb_log_file(alb_log_file)

    logger.info(alb_log_array[0].backend_ip)

