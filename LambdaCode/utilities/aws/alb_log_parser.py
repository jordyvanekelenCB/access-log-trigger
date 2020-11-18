""" This module contains the ALBLogParser class which is responsible for converting ALB log lines into a
list of ALB Log objects"""

import re
from models import ALBLog, ALBLogWebshop


class ALBLogParser:
    """ This class is responsible for converting ALB log lines into a list of ALB Log objects """

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def parse_alb_log_file_format_default(alb_log_file):
        """ Parse an alb log file into a list of ALB Log objects. Format: default """

        fields = [
            "type",
            "timestamp",
            "alb",
            "client_ip",
            "client_port",
            "backend_ip",
            "backend_port",
            "request_processing_time",
            "backend_processing_time",
            "response_processing_time",
            "alb_status_code",
            "backend_status_code",
            "received_bytes",
            "sent_bytes",
            "request_verb",
            "request_url",
            "request_proto",
            "user_agent",
            "ssl_cipher",
            "ssl_protocol",
            "target_group_arn",
            "trace_id",
            "domain_name",
            "chosen_cert_arn",
            "matched_rule_priority",
            "request_creation_time",
            "actions_executed",
            "redirect_url",
            "new_field",
        ]

        # Regex to parse ALB log file
        regex = r"([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*):([0-9]*) ([^ ]*)[:-]([0-9]*) ([-.0-9]*) ([-.0-9]*) ([-.0-9]*) " \
                r"(|[-0-9]*) (-|[-0-9]*) ([-0-9]*) ([-0-9]*) \"([^ ]*) ([^ ]*) (- |[^ ]*)\" \"([^\"]*)\" ([A-Z0-9-]+)" \
                r" ([A-Za-z0-9.-]*) ([^ ]*) \"([^\"]*)\" \"([^\"]*)\" \"([^\"]*)\" ([-.0-9]*) ([^ ]*) \"([^\"]*)\" " \
                r"($|\"[^ ]*\")(.*)"

        # Create list of objects
        alb_log_array = []

        for log_line in alb_log_file.split('\n'):

            # Get the regex matches from log line
            regex_matches = re.search(regex, log_line)

            if regex_matches:
                alb_log = ALBLog()

                for i, field in enumerate(fields):

                    # Set the attribute of the log file object with the value found with the regex
                    setattr(alb_log, field, regex_matches.group(i+1))

            alb_log_array.append(alb_log)

        return alb_log_array

    @staticmethod
    def parse_alb_log_file_format_webshop(alb_log_file):
        """ Parse an alb log file into a list of ALB Log objects. Format: webshop """

        # Create list of objects
        alb_log_array = []

        # Split log file into list of lines
        alb_log_file_list = alb_log_file.split('\n')

        # Remove first two and last lines from log
        del alb_log_file_list[0:2]
        del alb_log_file_list[-1]

        for alb_log_line in alb_log_file_list:

            # Split in tabs due to standard format
            alb_log_line_list = alb_log_line.split('\t')

            # Create new object and add to list
            alb_log_webshop_object = ALBLogWebshop(alb_log_line_list[0], alb_log_line_list[1], alb_log_line_list[2],
                                                   alb_log_line_list[3], alb_log_line_list[4], alb_log_line_list[5],
                                                   alb_log_line_list[6], alb_log_line_list[7], alb_log_line_list[8],
                                                   alb_log_line_list[9], alb_log_line_list[10], alb_log_line_list[11],
                                                   alb_log_line_list[12], alb_log_line_list[13], alb_log_line_list[14],
                                                   alb_log_line_list[15], alb_log_line_list[16], alb_log_line_list[17],
                                                   alb_log_line_list[18], alb_log_line_list[19], alb_log_line_list[20],
                                                   alb_log_line_list[21], alb_log_line_list[22], alb_log_line_list[23],
                                                   alb_log_line_list[24], alb_log_line_list[25], alb_log_line_list[26],
                                                   alb_log_line_list[27], alb_log_line_list[28], alb_log_line_list[29],
                                                   alb_log_line_list[30], alb_log_line_list[31], alb_log_line_list[32])

            alb_log_array.append(alb_log_webshop_object)

        return alb_log_array
