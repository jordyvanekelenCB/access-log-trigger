""" Unit test for ALB Log parser class """

import os
import sys
import inspect
# pylint: disable=E0401
import pytest

# Fix module import form parent directory error.
# Reference: https://stackoverflow.com/questions/55933630/
# python-import-statement-modulenotfounderror-when-running-tests-and-referencing
CURRENT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT_SRC = "%s/LambdaCode" % os.path.dirname(PROJECT_ROOT)

# Set up sys path
sys.path.insert(0, PROJECT_ROOT_SRC)

# Import project classes
# pylint: disable=C0413
from LambdaCode import app
from LambdaCode.connection.aws_dynamodb_connection import DynamoDBConnection
from LambdaCode.connection.aws_wafv2_connection import AWSWAFv2


def get_mock_config():
    """ Return the mocked config parser with arbitrary values of the components to be tested """

    # Create HTTP Flood config section
    config_section_http_flood_detection = {'HTTP_FLOOD_LOW_LEVEL_THRESHOLD': 1000,
                                           'HTTP_FLOOD_MEDIUM_LEVEL_THRESHOLD' : 5000,
                                           'HTTP_FLOOD_CRITICAL_LEVEL_THRESHOLD': 10000
                                           }
    # Create AWS WAF Config section
    config_section_aws_waf = {'IP_SET_BLOCKED_NAME': 'ip_set_blocked_test',
                              'IP_SET_BLOCKED_SCOPE': 'REGIONAL',
                              'IP_SET_BLOCKED_IDENTIFIER': '15d93a77-4031-4c0e-8744-3f8e21b15751'
                              }

    # Create DynamoDB config section
    config_section_dynamo_db = {'BLOCK_LIST_QUEUE_TABLE': 'block_list_queue_test'}

    # Mock Config parser
    mock_config = {'HTTP_FLOOD_DETECTION': config_section_http_flood_detection,
                   'AWS_WAF': config_section_aws_waf,
                   'DYNAMO_DB': config_section_dynamo_db
                   }

    return mock_config

@pytest.fixture(autouse=True)
def cleanup():
    """ Cleans up block list queue table and WAFv2 IP set before each integration test """

    # Get mock config
    mock_config = get_mock_config()

    # Get entries in DynamoDB table
    dynamodb_response = DynamoDBConnection(mock_config).get_from_queue()
    block_list_queue_entries = dynamodb_response['Items']

    # Create list of uuid's to be removed
    uuid_list = [item['uuid'] for item in block_list_queue_entries]

    # Remove all items
    DynamoDBConnection(mock_config).remove_from_queue(uuid_list)

    # Get locktoken from WAFv2
    wafv2_response = AWSWAFv2(mock_config).retrieve_ip_set()
    locktoken = wafv2_response['LockToken']

    # Update IP set with empty list
    AWSWAFv2(mock_config).update_ip_set([], locktoken)


def test_integration():
    """ Run integration test to make sure all AWS components are working together accordingly. Components being tested
     are S3, DynamoDB and Wafv2 """

    # !ARRANGE!

    # Mock Lambda event
    # pylint: disable=C0330
    mock_event = {'Records': [{'eventVersion': '2.0', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1',
                      'eventTime': '1970-01-01T00:00:00.000Z', 'eventName': 'ObjectCreated:Put',
                      'userIdentity': {'principalId': 'EXAMPLE'}, 'requestParameters': {'sourceIPAddress': '127.0.0.1'},
                      'responseElements': {'x-amz-request-id': 'EXAMPLE123456789'
                          , 'x-amz-id-2': 'EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH'},
                      's3': {'s3SchemaVersion': '1.0', 'configurationId': 'testConfigRule',
                             'bucket': {'name': 'test-alb-bucket2', 'ownerIdentity': {'principalId': 'EXAMPLE'},
                                        'arn': 'arn:aws:s3:::test-alb-bucket2'},
                             'object': {'key': 'AWSLogs/937333453566/elasticloadbalancing/eu-west-1/2020/11/16/93733345'
                                               '3566_elasticloadbalancing_eu-west-1_app.test-alb.2467b60e77f9d417_2020'
                                               '1116T1200Z_52.19.49.44_5pjqr6dy.log.gz',
                                        'size': 1024, 'eTag': '0123456789abcdef0123456789abcdef',
                                        'sequencer': '0A1B2C3D4E5F678901'}}}]}

    mock_config = get_mock_config()

    # Set the environment to test
    os.environ["APP_STATE"] = "test"

    # Set the app.CONFIG to mocked config parser
    app.CONFIG = mock_config

    # !ACT!

    # Call entry point
    app.lambda_handler(mock_event, None)

    # !ASSERT!

    # Retrieve item from DynamoDB
    dynamodb_response = DynamoDBConnection(mock_config).get_from_queue()
    block_list_queue_entries = dynamodb_response['Items']
    block_list_queue_entry = block_list_queue_entries[0]

    # Assert length of block list queue is one
    assert len(block_list_queue_entries) == 1

    # Assert block list queue entry has the right properties
    assert block_list_queue_entry['ip'] == '77.168.51.231'
    assert block_list_queue_entry['flood_level'] == 'flood_level_critical'
    assert str(block_list_queue_entry['uuid']).startswith('77.168.51.231')

    # Retrieve IP Set from WAFv2
    wafv2_response = AWSWAFv2(mock_config).retrieve_ip_set()
    block_list_entries = wafv2_response["IPSet"]["Addresses"]

    # Assert length of IP set is one
    assert len(block_list_entries) == 1

    # Assert IP set entry has the right IP address
    assert block_list_entries[0] == '77.168.51.231/32'
