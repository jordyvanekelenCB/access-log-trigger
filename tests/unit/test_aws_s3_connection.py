""" Unit test for AWSS3 class """

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
# pylint: disable=W0621
# pylint: disable=C0413
from LambdaCode.connection.aws_s3_connection import AWSS3


@pytest.fixture()
def get_mock_event():
    """ Return a mocked Lambda event with key of S3 object to be parsed """

    # Mock Lambda event
    # pylint: disable=C0330
    mock_event = {'Records': [{'eventVersion': '2.0', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1',
                               'eventTime': '1970-01-01T00:00:00.000Z', 'eventName': 'ObjectCreated:Put',
                               'userIdentity': {'principalId': 'EXAMPLE'}, 'requestParameters':
                                   {'sourceIPAddress': '127.0.0.1'},
                               'responseElements': {'x-amz-request-id': 'EXAMPLE1234    56789'
                                   , 'x-amz-id-2': 'EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH'},
                               's3': {'s3SchemaVersion': '1.0', 'configurationId': 'testConfigRule',
                                      'bucket': {'name': 'test-alb-bucket2', 'ownerIdentity': {'principalId': 'EXAMPLE'},
                                                 'arn': 'arn:aws:s3:::test-alb-bucket2'},
                                      'object': {'key': 'AWSLogs/937333453566/elasticloadbalancing/eu-west-1/2020/11/16/'
                                                        '937333453566_elasticloadbalancing_eu-west-1_app.test-alb.2467'
                                                        'b60e77f9d417_20201116T2020Z_52.19.49.44_4oz3460l.log.gz',
                                                 'size': 1024, 'eTag': '0123456789abcdef0123456789abcdef',
                                                 'sequencer': '0A1B2C3D4E5F678901'}}}]}

    return mock_event


def test_get_aws_log_file(get_mock_event):
    """ Test the get_aws_log_file and dependent class methods of AWSS3 class """

    # !ARRANGE!

    # !ACT!
    log_file = AWSS3(get_mock_event).get_aws_log_file()

    # !ASSERT!

    # Assert contents are right
    assert log_file == 'http 2020-11-16T20:17:46.014759Z app/test-alb/2467b60e77f9d417 64.227.99.233:40076 - -1 -1 -1 ' \
                       '400 - 0 272 "- http://test-alb-479516345.eu-west-1.elb.amazonaws.com:80- -" "-" - - - "-" "-" ' \
                       '"-" - 2020-11-16T20:17:45.862000Z "-" "-" "-" "-" "-" "-" "-"\n'
