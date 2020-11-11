import pytest
import sys, os, inspect
import configparser

# Fix module import form parent directory error.
# Reference: https://stackoverflow.com/questions/55933630/python-import-statement-modulenotfounderror-when-running-tests-and-referencing
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
project_root = os.path.dirname(current_dir)
project_root_src = "%s/LambdaCode"%os.path.dirname(project_root)

# Set up configuration path
config_path = os.path.join(os.path.dirname(project_root_src + "/LambdaCode"), 'config', 'config.ini')

# Set up sys path
sys.path.insert(0,project_root_src)

# Import project classes
from LambdaCode.http_flood import HTTPFlood
from LambdaCode.models.alb_log import ALBLog


@pytest.fixture()
def setup_alb_log_array():
    alb_log_array = []

    # Add client IP 1.1.1.1
    for number_of_requests in range(0, 1000):
        alb_log_client = ALBLog()
        alb_log_client.client_ip = '1.1.1.1'
        alb_log_array.append(alb_log_client)

        # Add client IP 2.2.2.2
    for number_of_requests in range(0, 10555):
        alb_log_client = ALBLog()
        alb_log_client.client_ip = '2.2.2.2'
        alb_log_array.append(alb_log_client)

        # Add client IP 3.3.3.3
    for number_of_requests in range(0, 7777):
        alb_log_client = ALBLog()
        alb_log_client.client_ip = '3.3.3.3'
        alb_log_array.append(alb_log_client)

    return alb_log_array


@pytest.fixture()
def setup_config():
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def test_parse_alb_log_to_dict(setup_alb_log_array, setup_config):

    # !ARRANGE!

    # Create HTTP Flood object
    http_flood_object = HTTPFlood(setup_config, setup_alb_log_array)

    # !ACT!
    ip_and_requests_dict = http_flood_object.parse_alb_log_to_dict(setup_alb_log_array)

    # !ASSERT!

    # Assert request values are correct
    assert ip_and_requests_dict['1.1.1.1'] == 1000
    assert ip_and_requests_dict['2.2.2.2'] == 10555
    assert ip_and_requests_dict['3.3.3.3'] == 7777

    # Assert dictionary has 3 keys
    assert len(ip_and_requests_dict) == 3


def test_translate_request_dict_to_alb_client_array(setup_alb_log_array):
    # !ARRANGE!

    # Create custom config object to control thresholds

    config = {'HTTP_FLOOD_DETECTION': {'HTTP_FLOOD_LOW_LEVEL_THRESHOLD': 100, 'HTTP_FLOOD_MEDIUM_LEVEL_THRESHOLD': 500,
                                       'HTTP_FLOOD_CRITICAL_LEVEL_THRESHOLD': 1000}}

    # Create HTTP Flood object
    http_flood_object = HTTPFlood(config, setup_alb_log_array)

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
