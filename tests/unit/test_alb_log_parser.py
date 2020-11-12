""" Unit test for ALB Log parser class """

import os
import sys
import inspect

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
from LambdaCode.utilities.aws.alb_log_parser import ALBLogParser


def test_parse_alb_log_file():
    """ Unit test test_parse_alb_log_file """

    # !ARRANGE!

    # Setup alb log file
    alb_log_file = 'http 2020-11-04T20:25:00.212749Z app/test-alb/2467b60e77f9d417 1.1.1.1:678 172.31.62.19:80 0.000' \
                   ' 0.000 0.000 200 200 149 269 "GET http://test-alb-479516345.eu-west-1.elb.amazonaws.com:80/' \
                   ' HTTP/1.1" "Python-urllib/3.8" - - arn:aws:elasticloadbalancing:eu-west-1:937333453566:targetgro' \
                   'up/test-alb-target-group/731b82150d9fdbd6 "Root=1-5fa30e1c-3c5b6c8a6ecb80ba184d5091" "-" "-" 0 2' \
                   '020-11-04T20:25:00.182000Z "forward" "-" "-" "172.31.62.19:80" "200" "-" "-"'

    # Setup ALB Log parser object
    alb_log_parser_object = ALBLogParser()

    # !ACT!
    alb_log_array = alb_log_parser_object.parse_alb_log_file(alb_log_file)
    alb_log_array_object = alb_log_array[0]

    # !ASSERT!
    assert len(alb_log_array) == 1
    assert alb_log_array_object.client_ip == '1.1.1.1'
    assert alb_log_array_object.client_port == '678'
    assert alb_log_array_object.backend_port == '80'
    assert alb_log_array_object.alb_status_code == '200'
    assert alb_log_array_object.backend_ip == '172.31.62.19'
    assert alb_log_array_object.request_url == 'http://test-alb-479516345.eu-west-1.elb.amazonaws.com:80/'
    assert alb_log_array_object.request_verb == 'GET'
    assert alb_log_array_object.request_proto == 'HTTP/1.1'
