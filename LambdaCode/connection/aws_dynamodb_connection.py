""" DynamoDB connection class """

import time
# pylint: disable=E0401
import boto3


class DynamoDBConnection:
    """ Handles all connections to DynamoDB """

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def bulk_insert_block_list_queue(self, alb_client_list):
        """ Inserts bulk data into list queue table """

        put_item_request_list = []

        for alb_client in alb_client_list:

            # Generate current timestamp
            timestamp_cur = int(time.time())

            # Generate uuid to conform to primary key restrictions
            uuid = alb_client.client_ip + '_' + str(timestamp_cur) + '_' + alb_client.http_flood_level.name

            # Add to put item request list
            put_item_request_list.append({
                'PutRequest' : {
                    'Item' : {
                        'uuid': uuid,
                        'ip': alb_client.client_ip,
                        'flood_level': alb_client.http_flood_level.name,
                        'timestamp_start': timestamp_cur
                    }
                }
            })

        # Divide put_item_request_list into chunks of smaller list because bulk_insert limit is 25 per request:
        put_item_request_chunks_list = [put_item_request_list[x:x+25] for x in range(0, len(put_item_request_list), 25)]

        for put_item_request_chunk in put_item_request_chunks_list:
            self.dynamodb.batch_write_item(RequestItems={
                'block_list_queue': put_item_request_chunk
            })

    def insert_block_list_queue_entry(self, ip_address, flood_level):
        """ Inserts entry in block-list queue """

        table_block_list_queue = self.dynamodb.Table('block_list_queue')

        # Generate current timestamp
        timestamp_cur = int(time.time())

        # Generate uuid to conform to primary key restrictions
        uuid = ip_address + '_' + str(timestamp_cur) + '_' + flood_level

        # Insert item and get response
        table_block_list_queue.put_item(Item={
            'uuid': uuid,
            'ip': ip_address,
            'flood_level': flood_level,
            'timestamp_start': timestamp_cur
        })

    def retrieve_block_list_queue(self):
        """ Retrieves all entries from the block-list queue """

        table_block_list_queue = self.dynamodb.Table('block_list_queue')

        # Return all entries from database
        block_list_entries = table_block_list_queue.scan()

        return block_list_entries

    def remove_items_block_list_queue(self, uuid_list_expired):
        """ Removes an item from the block-list queue by a given list of uuid's """

        table_block_list_queue = self.dynamodb.Table('block_list_queue')

        for uuid in uuid_list_expired:
            table_block_list_queue.delete_item(Key={
                'uuid': uuid
            })
