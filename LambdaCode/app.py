import logging
import boto3
from helper import AWSS3
from helper import ALBLogParser
from http_flood import HTTPFlood

# Setup boto3 session
session = boto3.Session()

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# TODO: write tests, implement clean architecture, think about putting in more than 1 project, what to do with results

"""
Notes: 

Een optie is om de interval te verhogen van 5 naar bijv. een uur, het nadeel hiervan is dat een aanval dan pas na een uur gedetecteerd kan worden

"""


def lambda_handler(event, context):

    # Create boto3 s3 client
    boto_s3_client = boto3.client('s3')

    # Instantiate aws s3 helper
    aws_s3_helper = AWSS3(event, boto_s3_client)
    alb_log_parser_helper = ALBLogParser()

    # Retrieve alb log file
    alb_log_file = aws_s3_helper.get_aws_log_file()

    # Parse alb log file into array of objects
    alb_log_array = alb_log_parser_helper.parse_alb_log_file(alb_log_file)

    # Activate HTTP flood detection
    http_flood = HTTPFlood(alb_log_array)
    http_flood_results = http_flood.detect_http_flood()

    print_results(http_flood_results)

# TODO delete this
def print_results(http_flood_results):

    for parsed_alb_client in http_flood_results:

        logger.info("Finding: " + "Client ip: " + parsed_alb_client.client_ip + ' | Flood level: ' + str(parsed_alb_client.http_flood_level.name) + ' | Number of requests: ' + str(parsed_alb_client.number_of_requests))
