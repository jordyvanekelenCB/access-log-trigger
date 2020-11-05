from connection.dynamodb_connection import DynamoDBConnection
import logging
import time
from helper import AWSWAFv2
import datetime

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class HTTPFloodClean:

    config_section_http_flood_clean = 'HTTP_FLOOD_CLEAN'

    def __init__(self, config):
        self.config = config

        self.http_flood_low_level_timeout = int(self.config[self.config_section_http_flood_clean]['HTTP_FLOOD_LOW_LEVEL_TIMEOUT'])
        self.http_flood_medium_level_timeout = int(self.config[self.config_section_http_flood_clean]['HTTP_FLOOD_MEDIUM_LEVEL_TIMEOUT'])
        self.http_flood_critical_level_timeout = int(self.config[self.config_section_http_flood_clean]['HTTP_FLOOD_CRITICAL_LEVEL_TIMEOUT'])

    def clean_http_flood(self):

        block_list_queue = self.retrieve_blocklist_queue()
        block_list_queue_expired = self.filter_block_list_queue(block_list_queue)
        self.remove_items_from_block_list(block_list_queue_expired)

        return block_list_queue_expired

    def retrieve_blocklist_queue(self):

        # Get block list entries to be removed
        block_list_queue = DynamoDBConnection().retrieve_block_list_queue()

        return block_list_queue

    def filter_block_list_queue(self, block_list_queue):

        block_list_queue_items = block_list_queue["Items"]
        block_list_queue_expired = {'Items': []}

        for item in block_list_queue_items:
            timestamp_start = int(item['timestamp_start'])
            flood_level = item['flood_level']

            if flood_level == 'flood_level_low':
                if int(time.time()) > timestamp_start + self.http_flood_low_level_timeout * 60:
                    block_list_queue_expired['Items'].append(item)
                else:
                    continue
            elif flood_level == 'flood_level_medium':
                if int(time.time()) > timestamp_start + self.http_flood_medium_level_timeout * 60:
                    block_list_queue_expired['Items'].append(item)
                else:
                    continue
            elif flood_level == 'flood_level_critical':

                # For debugging purposes
                now = int(time.time())
                attack_detected = timestamp_start + self.http_flood_critical_level_timeout * 60

                now_readable = datetime.datetime.utcfromtimestamp(now).strftime('%Y-%m-%dT%H:%M:%SZ')
                attack_detected_readable = datetime.datetime.utcfromtimestamp(attack_detected).strftime('%Y-%m-%dT%H:%M:%SZ')

                if int(now) > int(attack_detected):
                    block_list_queue_expired['Items'].append(item)
                    logger.info(now_readable + ' | ' + attack_detected_readable)


                else:
                    continue

        return block_list_queue_expired

    def remove_items_from_block_list(self, block_list_queue_expired):

        # Get IP set, then update IP Set
        aws_waf_v2_helper = AWSWAFv2(self.config);
        ip_set_response = aws_waf_v2_helper.retrieve_ip_set()

        current_blocklist_addresses = ip_set_response["IPSet"]["Addresses"]
        locktoken = ip_set_response["LockToken"]

        ips_to_be_removed = []

        # Parse database response
        for item in block_list_queue_expired['Items']:
            ips_to_be_removed.append(item['ip'] + '/32')

        # Create list of uuid's to be removed
        uuid_list_expired = []

        for item in block_list_queue_expired['Items']:
            uuid_list_expired.append(item['uuid'])

        # New blocklist = current_blocklist - ips_to_be_removed
        new_blocklist = [ip for ip in current_blocklist_addresses if ip not in ips_to_be_removed]

        # Update current IP Set with new blocklist
        aws_waf_v2_helper.update_ip_set(new_blocklist, locktoken)

        # Remove removed items from database queue
        DynamoDBConnection().remove_items_block_list_queue(uuid_list_expired)