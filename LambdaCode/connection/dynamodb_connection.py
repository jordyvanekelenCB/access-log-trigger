import boto3
import time
import logging

# Setup logger
logger = logging.getLogger()


class DynamoDBConnection:

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def put_block_list_queue_entry(self, ip, flood_level):

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

        logger.info(response)


