""" ALBClient model """

# pylint: disable=R0903
class ALBClient:
    """ This class acts as a model for ALBClient """

    def __init__(self, client_ip, number_of_requests, http_flood_level):

        self.client_ip = client_ip
        self.number_of_requests = number_of_requests
        self.http_flood_level = http_flood_level
