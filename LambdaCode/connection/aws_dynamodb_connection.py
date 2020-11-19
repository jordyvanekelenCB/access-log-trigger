""" DynamoDB connection class """

import time
# pylint: disable=E0401
import boto3
from interfaces.iqueuedatabase import IQueueDatabase


class DynamoDBConnection(IQueueDatabase):
    """ Handles all connections to DynamoDB, implements interface IQueueDatabase """

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def insert_into_queue(self, client_list) -> None:
        """ Inserts bulk data into list queue table """

        put_item_request_list = []

        for alb_client in client_list:

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

    def get_from_queue(self) -> list:
        pass

    def remove_from_queue(self, client_list):
        pass
