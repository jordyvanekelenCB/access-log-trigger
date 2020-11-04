import logging
from connection.aws_connection import AWSConnection
import os

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class AWSWAFv2:

    config_section_waf = 'AWS_WAF'

    def __init__(self, config):
        self.boto_wafv2_client = AWSConnection().get_connection('wafv2')

        # Retrieve config parser
        self.config = config

        # Read config file from relative path
        self.config.read(os.path.join(os.path.dirname(__file__), 'config', 'config.ini'))

        # Setup instance attributes
        self.ip_set_blocked_name = self.config[self.config_section_waf]['IP_SET_BLOCKED_NAME']
        self.ip_set_blocked_scope = self.config[self.config_section_waf]['IP_SET_BLOCKED_SCOPE']
        self.ip_set_blocked_identifier = self.config[self.config_section_waf]['IP_SET_BLOCKED_IDENTIFIER']


    def retrieve_ip_set(self):

        # Get IP block list
        response = self.boto_wafv2_client.get_ip_set(Name=self.ip_set_blocked_name, Scope=self.ip_set_blocked_scope,
                                                     Id=self.ip_set_blocked_identifier)

        logger.info(response)
        # Get IPv4/IPv6 addresses from block list

        return response

    def update_ip_set(self, alb_client_array):

        # Retrieve the current IPSet
        response = self.retrieve_ip_set()

        blocklist_addresses = response["IPSet"]["Addresses"]
        locktoken = response["LockToken"]

        for alb_client in alb_client_array:

            if alb_client.flood_level.value == 'flood_level_none':
                continue

            blocklist_addresses.append(alb_client.client_ip + '/32')  # Add a single IP address

        response = self.boto_wafv2_client.update_ip_set(Name=self.ip_set_blocked_name, Scope=self.ip_set_blocked_scope, Id=self.ip_set_blocked_identifier,
                                             Addresses=blocklist_addresses, LockToken=locktoken)

        logger.info(blocklist_addresses)


