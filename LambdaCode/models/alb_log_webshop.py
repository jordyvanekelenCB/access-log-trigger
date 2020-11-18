""" ALB Log default model """


# pylint: disable=R0902
# pylint: disable=R0903
# pylint: disable=R0914
class ALBLogWebshop:
    """ This class acts as an ALB Log default model """

    # pylint: disable=R0913
    def __init__(self, date, time, x_edge_location, sc_bytes, client_ip, cs_method, cs_host, cs_uri_stem, sc_status,
                 cs_referer, cs_user_agent, cs_uri_query, cs_cookie, x_edge_result_type, x_edge_request_id,
                 x_host_header, cs_protocol, cs_bytes, time_taken, x_forwarded_for, ssl_protocol, ssl_cipher,
                 x_edge_response_result_type, cs_protocol_version, fle_status, fle_encrypted_fields, c_port,
                 time_to_first_byte, x_edge_detailed_result_type, sc_content_type, sc_content_len, sc_range_start,
                 sc_range_end):

        self.date = date
        self.time = time
        self.x_edge_location = x_edge_location
        self.sc_bytes = sc_bytes
        self.client_ip = client_ip
        self.cs_method = cs_method
        self.cs_host = cs_host
        self.cs_uri_stem = cs_uri_stem
        self.sc_status = sc_status
        self.cs_referer = cs_referer
        self.cs_user_agent = cs_user_agent
        self.cs_uri_query = cs_uri_query
        self.cs_cookie = cs_cookie
        self.x_edge_result_type = x_edge_result_type
        self.x_edge_request_id = x_edge_request_id
        self.x_host_header = x_host_header
        self.cs_protocol = cs_protocol
        self.cs_bytes = cs_bytes
        self.time_taken = time_taken
        self.x_forwarded_for = x_forwarded_for
        self.ssl_protocol = ssl_protocol
        self.ssl_cipher = ssl_cipher
        self.x_edge_response_result_type = x_edge_response_result_type
        self.cs_protocol_version = cs_protocol_version
        self.fle_status = fle_status
        self.fle_encrypted_fields = fle_encrypted_fields
        self.c_port = c_port
        self.time_to_first_byte = time_to_first_byte
        self.x_edge_detailed_result_type = x_edge_detailed_result_type
        self.sc_content_type = sc_content_type
        self.sc_content_len = sc_content_len
        self.sc_range_start = sc_range_start
        self.sc_range_end = sc_range_end


    date = ''
    time = ''
    x_edge_location = ''
    sc_bytes = ''
    client_ip = ''
    cs_method = ''
    cs_host = ''
    cs_uri_stem = ''
    sc_status = ''
    cs_referer = ''
    cs_user_agent = ''
    cs_uri_query = ''
    cs_cookie = ''
    x_edge_result_type = ''
    x_edge_request_id = ''
    x_host_header = ''
    cs_protocol = ''
    cs_bytes = ''
    time_taken = ''
    x_forwarded_for = ''
    ssl_protocol = ''
    ssl_cipher = ''
    x_edge_response_result_type = ''
    cs_protocol_version = ''
    fle_status = ''
    fle_encrypted_fields = ''
    c_port = ''
    time_to_first_byte = ''
    x_edge_detailed_result_type = ''
    sc_content_type = ''
    sc_content_len = ''
    sc_range_start = ''
    sc_range_end = ''
