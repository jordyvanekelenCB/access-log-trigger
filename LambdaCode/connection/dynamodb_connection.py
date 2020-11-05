import boto3
import time
import logging
from boto3.dynamodb.conditions import Key, Attr

# Setup logger
logger = logging.getLogger()


class DynamoDBConnection:

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def insert_block_list_queue_entry(self, ip, flood_level):

        table_block_list_queue = self.dynamodb.Table('block_list_queue')

        # Generate current timestamp
        timestamp_cur = int(time.time())

        # Generate uuid to conform to primary key restrictions
        uuid = ip + '_' + str(timestamp_cur) + '_' + flood_level

        # Insert item and get response
        response = table_block_list_queue.put_item(Item={
            'uuid': uuid,
            'ip': ip,
            'flood_level': flood_level,
            'timestamp_start': timestamp_cur
        })


    def retrieve_block_list_queue(self, low_level_flood_timeout):
        table_block_list_queue = self.dynamodb.Table('block_list_queue')

        # Get all items to be removed | thus, timestamp_start < timestamp_now - minimum flood_level
        #timestamp_now - flood_level_time = nu: 13:00-10 minuten, 12:45
        #12:45 -> low level flood + 10 = 12:55
        #12:45 -> critical_flood + 30 = 13:15
        #13:10 -> scan, 13:10 - 10 = 13:00, 12:55<13:00? 13:15<13:00

        #13:00 -> scan, dus 13:00-10=12:55, dus select * now where timestamp_start < (to_be_removed) timestamp_now - low_level_flood
        #To test, have two IPs, 1 make low level threshold, two, critical threshold.

        timestamp_expression = int(time.time()) - low_level_flood_timeout*60
        #timestamp_expression = int(time.time()) - 60*60*8

        block_list_entries = table_block_list_queue.scan(
        )

        return block_list_entries


    def remove_items_block_list_queue(self, uuid_list_expired):
        table_block_list_queue = self.dynamodb.Table('block_list_queue')

        for uuid in uuid_list_expired:
            response = table_block_list_queue.delete_item(Key={
                'uuid': uuid
            })
