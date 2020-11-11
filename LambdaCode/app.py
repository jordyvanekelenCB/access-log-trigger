import logging
from utilities import ALBLogParser
from connection.aws_s3_connection import AWSS3
from http_flood import HTTPFlood
import configparser
import os

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Setup config parser
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config', 'config.ini'))

def lambda_handler(event, context):

    # Instantiate aws s3 helper
    aws_s3_helper = AWSS3(event)
    alb_log_parser_helper = ALBLogParser()

    # Retrieve alb log file
    alb_log_file = aws_s3_helper.get_aws_log_file()

    # Parse alb log file into array of objects
    alb_log_array = alb_log_parser_helper.parse_alb_log_file(alb_log_file)

    # Activate HTTP flood detection
    http_flood = HTTPFlood(config, alb_log_array)
    http_flood_results = http_flood.detect_http_flood()

    # Print results
    print_results(http_flood_results)


def print_results(http_flood_results):

    logger.info('================================ Http flood detection results ================================')

    for parsed_alb_client in http_flood_results:
        logger.info("Finding: " + "Client ip: " + parsed_alb_client.client_ip + ' | Flood level: ' + str(parsed_alb_client.http_flood_level.name) + ' | Number of requests: ' + str(parsed_alb_client.number_of_requests))


