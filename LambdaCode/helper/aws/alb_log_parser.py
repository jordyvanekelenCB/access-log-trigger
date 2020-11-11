import re, sys
from models import ALBLog;
import logging

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ALBLogParser:

    def parse_alb_log_file(self, alb_log_file):

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
        regex = r"([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*):([0-9]*) ([^ ]*)[:-]([0-9]*) ([-.0-9]*) ([-.0-9]*) ([-.0-9]*) (|[-0-9]*) (-|[-0-9]*) ([-0-9]*) ([-0-9]*) \"([^ ]*) ([^ ]*) (- |[^ ]*)\" \"([^\"]*)\" ([A-Z0-9-]+) ([A-Za-z0-9.-]*) ([^ ]*) \"([^\"]*)\" \"([^\"]*)\" \"([^\"]*)\" ([-.0-9]*) ([^ ]*) \"([^\"]*)\" ($|\"[^ ]*\")(.*)"

        # Create list of objects
        alb_log_array = []

        for log_line in alb_log_file.split('\n'):

            # Get the regex matches from log line
            regex_matches = re.search(regex, log_line)

            if regex_matches:
                alb_log = ALBLog();

                for i, field in enumerate(fields):

                    # Set the attribute of the log file object with the value found with the regex
                    setattr(alb_log, field, regex_matches.group(i+1))

            alb_log_array.append(alb_log)

        return alb_log_array

    pass
