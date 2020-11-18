"""
Entry point file
"""
import os
import logging
import configparser
from utilities import ALBLogParser
from connection.aws_s3_connection import AWSS3
from http_flood import HTTPFlood

# Setup logger
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# Setup config parser
CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'config', 'config.ini'))

# pylint: disable=W0613
def lambda_handler(event, context):
    """ Entry point of the application"""

    # Instantiate aws s3 helper
    aws_s3_helper = AWSS3(event)
    alb_log_parser_helper = ALBLogParser()

    # Retrieve alb log file
    alb_log_file = aws_s3_helper.get_aws_log_file()

    # Parse alb log file into array of objects
    alb_log_array = alb_log_parser_helper.parse_alb_log_file_format_webshop(alb_log_file)

    # Activate HTTP flood detection
    http_flood = HTTPFlood(CONFIG, alb_log_array)
    http_flood_results = http_flood.detect_http_flood()

    # Print results
    print_results(http_flood_results)


def print_results(http_flood_results):
    """ Prints the results of the http flood detection module """

    LOGGER.info('================================ Http flood detection results ================================')

    for parsed_alb_client in http_flood_results:

        # pylint: disable=W1202
        LOGGER.info("Finding: Client ip: {0} | Flood level: {1} | Number of requests: {2}"
                    .format(parsed_alb_client.client_ip, parsed_alb_client.http_flood_level.name,
                            parsed_alb_client.number_of_requests))
