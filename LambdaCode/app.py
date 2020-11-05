import logging
from helper import AWSS3, ALBLogParser, AWSWAFv2
from http_flood import HTTPFlood
import configparser
import os
from http_flood_clean import HTTPFloodClean
import datetime

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Setup config parser
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config', 'config.ini'))

# TODO: write tests, implement clean architecture, think about putting in more than 1 project, what to do with results

"""
Notes: 

Een optie is om de interval te verhogen van 5 naar bijv. een uur, het nadeel hiervan is dat een aanval dan pas na een uur gedetecteerd kan worden

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wafv2.html?highlight=wafv2#WAFV2.Client.get_ip_set

https://github.com/awslabs/aws-waf-security-automations/blob/d7e42d69c77cead0bb31a41e4a69cf8667884253/source/lib/waflibv2.py#L101

Update IP SET? Get old one, merge with new one? 

"""


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

    # Activate HTTP flood clean
    http_clean_results = HTTPFloodClean(config).clean_http_flood()

    print_results(config, http_flood_results, http_clean_results)



# TODO delete this
def print_results(config, http_flood_results, http_clean_results):

    logger.info('================================ Http flood detection results ================================')
    for parsed_alb_client in http_flood_results:
        logger.info("Finding: " + "Client ip: " + parsed_alb_client.client_ip + ' | Flood level: ' + str(parsed_alb_client.http_flood_level.name) + ' | Number of requests: ' + str(parsed_alb_client.number_of_requests))


    logger.info('')

    logger.info('================================ Http flood clean results ================================')
    for item in http_clean_results['Items']:
        readable_time = datetime.datetime.utcfromtimestamp(item['timestamp_start']).strftime('%Y-%m-%dT%H:%M:%SZ')
        logger.info("Finding : Removed client ip: " + item['ip'] + " | Flood level: " + item['flood_level'] + " | Time attack detected: " + readable_time)



