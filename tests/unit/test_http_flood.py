""" Unit test for HTTP Flood class """


import sys
import os
import inspect
import configparser
# pylint: disable=E0401
import pytest

# Fix module import form parent directory error.
# Reference: https://stackoverflow.com/questions/55933630/
# python-import-statement-modulenotfounderror-when-running-tests-and-referencing
CURRENT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT_SRC = "%s/LambdaCode" % os.path.dirname(PROJECT_ROOT)

# Set up configuration path
CONFIG_PATH = os.path.join(os.path.dirname(PROJECT_ROOT_SRC + "/LambdaCode"), 'config', 'config.ini')

# Set up sys path
sys.path.insert(0, PROJECT_ROOT_SRC)

# Import project classes
# pylint: disable=C0413
from LambdaCode.http_flood import HTTPFlood
from LambdaCode.models.alb_log_default import ALBLog


@pytest.fixture()
def setup_alb_log_list():
    """ This fixture returns a list containing ALB Log objects"""

    alb_log_list = []

    # Add client IP 1.1.1.1
    # pylint: disable=W0612
    for number_of_requests in range(0, 1000):
        alb_log = ALBLog()
        alb_log.client_ip = '1.1.1.1'
        alb_log_list.append(alb_log)

        # Add client IP 2.2.2.2
    for number_of_requests in range(0, 10555):
        alb_log = ALBLog()
        alb_log.client_ip = '2.2.2.2'
        alb_log_list.append(alb_log)

        # Add client IP 3.3.3.3
    for number_of_requests in range(0, 7777):
        alb_log = ALBLog()
        alb_log.client_ip = '3.3.3.3'
        alb_log_list.append(alb_log)

    return alb_log_list


@pytest.fixture()
def setup_config():
    """ Fixture for setting up configuration parser """

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    return config

# pylint: disable=W0621
def test_parse_alb_log_to_dict(setup_alb_log_list, setup_config):
    """ Unit test for parse_alb_log_to_dict class method"""

    # !ARRANGE!

    # Create HTTP Flood object
    http_flood_object = HTTPFlood(setup_config, setup_alb_log_list)

    # !ACT!
    ip_and_requests_dict = http_flood_object.parse_alb_log_to_dict(setup_alb_log_list)

    # !ASSERT!

    # Assert request values are correct
    assert ip_and_requests_dict['1.1.1.1'] == 1000
    assert ip_and_requests_dict['2.2.2.2'] == 10555
    assert ip_and_requests_dict['3.3.3.3'] == 7777

    # Assert dictionary has 3 keys
    assert len(ip_and_requests_dict) == 3


def test_translate_request_dict_to_alb_client_array(setup_alb_log_list):
    """ Unit test for translate_request_dict_to_alb_client_array class method"""

    # !ARRANGE!

    # Create custom config object to control thresholds

    config = {'HTTP_FLOOD_DETECTION': {'HTTP_FLOOD_LOW_LEVEL_THRESHOLD': 100, 'HTTP_FLOOD_MEDIUM_LEVEL_THRESHOLD': 500,
                                       'HTTP_FLOOD_CRITICAL_LEVEL_THRESHOLD': 1000}}

    # Create HTTP Flood object
    http_flood_object = HTTPFlood(config, setup_alb_log_list)

    # Create dictionary and setup values
    ip_and_requests_dict = {'1.1.1.1': 50, '2.2.2.2': 150, '3.3.3.3': 550, '4.4.4.4': 1050}

    # !ACT!
    alb_client_array = http_flood_object.translate_request_dict_to_alb_client_array(ip_and_requests_dict)

    # !ASSERT!
    for alb_client in alb_client_array:
        if alb_client.client_ip == '1.1.1.1':
            assert alb_client.http_flood_level == HTTPFlood.HTTPFloodLevel.flood_level_none
        if alb_client.client_ip == '2.2.2.2':
            assert alb_client.http_flood_level == HTTPFlood.HTTPFloodLevel.flood_level_low
        if alb_client.client_ip == '3.3.3.3':
            assert alb_client.http_flood_level == HTTPFlood.HTTPFloodLevel.flood_level_medium
        if alb_client.client_ip == '4.4.4.4':
            assert alb_client.http_flood_level == HTTPFlood.HTTPFloodLevel.flood_level_critical
