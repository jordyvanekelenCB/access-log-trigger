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

    alb_client_http_flood_none_list = []
    alb_client_http_flood_low_list = []
    alb_client_http_flood_medium_list = []
    alb_client_http_flood_critical_list = []

    for parsed_alb_client in http_flood_results:

        if parsed_alb_client.http_flood_level.name == 'flood_level_none':
            alb_client_http_flood_none_list.append(parsed_alb_client)
        elif parsed_alb_client.http_flood_level.name == 'flood_level_low':
            alb_client_http_flood_low_list.append(parsed_alb_client)
        elif parsed_alb_client.http_flood_level.name == 'flood_level_medium':
            alb_client_http_flood_medium_list.append(parsed_alb_client)
        elif parsed_alb_client.http_flood_level.name == 'flood_level_critical':
            alb_client_http_flood_critical_list.append(parsed_alb_client)

    # pylint: disable=W1202
    LOGGER.info('Total number of clients: {0}'.format(len(http_flood_results)))
    LOGGER.info('None level flood detections: {0}'.format(len(alb_client_http_flood_none_list)))
    LOGGER.info('Low level flood detections: {0}'.format(len(alb_client_http_flood_low_list)))
    LOGGER.info('Medium level flood detections: {0}'.format(len(alb_client_http_flood_medium_list)))
    LOGGER.info('Critical level flood detections: {0}'.format(len(alb_client_http_flood_critical_list)))
