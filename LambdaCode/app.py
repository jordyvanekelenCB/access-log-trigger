"""
Entry point file
"""
import os
import logging
import configparser
from utilities import ALBLogParser, Diagnostics
from connection.aws_s3_connection import AWSS3
from http_flood import HTTPFlood

# Setup logger
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# Setup config parser
CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'config', 'config.ini'))


# pylint: disable=W0613
def lambda_handler(event, context) -> None:
    """ Entry point of the application"""

    # Get application state to determine testing/production
    application_state = os.environ['APP_STATE']

    # Instantiate aws s3 helper
    aws_s3_helper = AWSS3(event)
    alb_log_parser_helper = ALBLogParser()

    # Retrieve alb log file
    alb_log_file = aws_s3_helper.get_aws_log_file()

    # Initialize empty log array
    alb_log_array = []

    # Parse alb log file into array of objects
    if application_state == 'production':
        alb_log_array = alb_log_parser_helper.parse_alb_log_file_format_webshop(alb_log_file)
    elif application_state == 'test':
        alb_log_array = alb_log_parser_helper.parse_alb_log_file_format_default(alb_log_file)
    else:
        raise Exception('Error: no application state env variable has been set or has other value than "production" '
                        'or "test". Exiting!')

    # Log application state
    # pylint: disable=W1202
    LOGGER.info('Detected application state: {0}'.format(application_state))

    # Activate HTTP flood detection
    http_flood = HTTPFlood(CONFIG, alb_log_array)
    http_flood_results = http_flood.detect_http_flood()

    # Print results
    Diagnostics.print_results(http_flood_results)
