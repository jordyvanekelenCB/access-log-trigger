""" This module contains the HTTPFlood class which is reponsible for detecting HTTP flood attacks in log files """

from enum import Enum
from models.alb_client import ALBClient
from connection.aws_wafv2_connection import AWSWAFv2
from connection.aws_dynamodb_connection import DynamoDBConnection


class HTTPFlood:
    """ This class is responsible for finding detecting HTTP flood attacks in log files """

    config_section_http_flood = 'HTTP_FLOOD_DETECTION'

    def __init__(self, config, alb_log_array):
        self.alb_log_array = alb_log_array

        # Setup config parser
        self.config = config

        # Setup instance attributes
        self.http_flood_low_level_threshold = \
            int(self.config[self.config_section_http_flood]['HTTP_FLOOD_LOW_LEVEL_THRESHOLD'])
        self.http_flood_medium_level_threshold = \
            int(self.config[self.config_section_http_flood]['HTTP_FLOOD_MEDIUM_LEVEL_THRESHOLD'])
        self.http_flood_critical_level_threshold = \
            int(self.config[self.config_section_http_flood]['HTTP_FLOOD_CRITICAL_LEVEL_THRESHOLD'])

    def detect_http_flood(self) -> list:

        """ This is the main function """

        # Parse alb log to dictionary with ip:number_of_requests
        ip_and_requests_dict = self.parse_alb_log_to_dict(self.alb_log_array)

        # Translate number of requests for each ip to http flood level
        alb_client_array = self.translate_request_dict_to_alb_client_array(ip_and_requests_dict)

        # Get current block_list
        ip_set_response = AWSWAFv2(self.config).retrieve_ip_set()
        current_blocklist_addresses = ip_set_response["IPSet"]["Addresses"]
        locktoken = ip_set_response["LockToken"]

        # Filter out http_flood_none level to update IP set
        wafv2_alb_client_addresses = []
        db_alb_client_list = []

        for alb_client in alb_client_array:
            if alb_client.http_flood_level.value != 'flood_level_none':
                wafv2_alb_client_addresses.append(alb_client.client_ip + '/32')
                db_alb_client_list.append(alb_client)

        # Merge old block list with new ips
        new_block_list_addresses = current_blocklist_addresses + wafv2_alb_client_addresses

        # Update IP Set after getting alb client results
        AWSWAFv2(self.config).update_ip_set(new_block_list_addresses, locktoken)

        # Save items to database implementation so IP's can be removed after a certain period of time
        DynamoDBConnection(self.config).insert_into_queue(db_alb_client_list)

        return alb_client_array

    @staticmethod
    def parse_alb_log_to_dict(alb_log_array) -> dict:
        """ Parses a list of ALB Log items into a dictionary with client IP and number of requests """

        ip_and_requests_dict = {}

        for alb_log in alb_log_array:
            if alb_log.client_ip not in ip_and_requests_dict:
                ip_and_requests_dict[alb_log.client_ip] = 1
            else:
                ip_and_requests_dict[alb_log.client_ip] += 1

        return ip_and_requests_dict

    def translate_request_dict_to_alb_client_array(self, ip_and_requests_dict) -> list:
        """ Translates dictionary with client IP and number of requests to a list of ALB client objects and converts
            the number of requests to the according flood level
         """

        alb_client_list = []

        for client_ip in ip_and_requests_dict:

            number_of_requests = ip_and_requests_dict.get(client_ip)

            # Converts number of requests to HTTP flood level
            if number_of_requests < self.http_flood_low_level_threshold:
                alb_client_list.append(ALBClient(client_ip, number_of_requests, self.HTTPFloodLevel.flood_level_none))
            elif self.http_flood_low_level_threshold <= number_of_requests < self.http_flood_medium_level_threshold:
                alb_client_list.append(ALBClient(client_ip, number_of_requests, self.HTTPFloodLevel.flood_level_low))
            elif self.http_flood_medium_level_threshold <= number_of_requests < \
                    self.http_flood_critical_level_threshold:
                alb_client_list.append(ALBClient(client_ip, number_of_requests, self.HTTPFloodLevel.flood_level_medium))
            elif number_of_requests >= self.http_flood_critical_level_threshold:
                alb_client_list.append(ALBClient(client_ip, number_of_requests, self.HTTPFloodLevel.flood_level_critical))

        return alb_client_list

    class HTTPFloodLevel(Enum):
        """ Subclass enum for HTTPFloodLevel """
        flood_level_none = 'flood_level_none'
        flood_level_low = 'flood_level_low'
        flood_level_medium = 'flood_level_medium'
        flood_level_critical = 'flood_level_critical'
