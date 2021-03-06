""" ALB Log default model """


# pylint: disable=R0903
class ALBLog:
    """ This class acts as an ALB Log default model """

    type = ''
    timestmp = ''
    alb = ''
    client_ip = ''
    client_port = ''
    backend_ip = ''
    backend_port = ''
    request_processing_time = ''
    backend_processing_time = ''
    response_processing_time = ''
    alb_status_code = ''
    backend_status_code = ''
    received_bytes = ''
    sent_bytes = ''
    request_verb = ''
    request_url = ''
    request_proto = ''
    user_agent = ''
    ssl_cipher = ''
    ssl_protocol = ''
    target_group_arn = ''
    trace_id = ''
    domain_name = ''
    chosen_cert_arn = ''
    matched_rule_priority = ''
    request_creation_time = ''
    redirect_url = ''
    new_field = ''
