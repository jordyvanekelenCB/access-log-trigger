""" This module holds the PrintResults class """

import logging

# Setup logger
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class Diagnostics:
    """ This class is responsible for printing diagnostic results """

    def __str__(self):
        return self.__class__.__name__

    # pylint: disable=R0912
    @staticmethod
    def print_results(http_flood_results) -> None:
        """ Prints the results of the http flood detection module """

        LOGGER.info('================================ Http flood detection results ================================')

        alb_client_http_flood_none_list = []
        alb_client_http_flood_low_list = []
        alb_client_http_flood_medium_list = []
        alb_client_http_flood_critical_list = []

        for parsed_alb_client in http_flood_results:

            if parsed_alb_client.http_flood_level.name == 'flood_level_none':
                alb_client_http_flood_none_list.append(parsed_alb_client)
            elif parsed_alb_client.http_flood_level.name == 'flood_level_low':
                alb_client_http_flood_low_list.append(parsed_alb_client)
            elif parsed_alb_client.http_flood_level.name == 'flood_level_medium':
                alb_client_http_flood_medium_list.append(parsed_alb_client)
            elif parsed_alb_client.http_flood_level.name == 'flood_level_critical':
                alb_client_http_flood_critical_list.append(parsed_alb_client)

        LOGGER.info('--------------------------- [General information] ---------------------------')

        # pylint: disable=W1202
        LOGGER.info('Total number of clients: {0}.'.format(len(http_flood_results)))

        if alb_client_http_flood_low_list:
            LOGGER.info('Low level flood detections: {0}. Action taken: Added to IP set and queue.'.
                        format(len(alb_client_http_flood_low_list)))
        else:
            LOGGER.info('Low level flood detections: 0.')

        if alb_client_http_flood_medium_list:
            LOGGER.info('Medium level flood detections: {0}. Action taken: Added to IP set and queue.'.
                        format(len(alb_client_http_flood_medium_list)))
        else:
            LOGGER.info('Medium level flood detections: 0.')

        if alb_client_http_flood_critical_list:
            LOGGER.info('Critical level flood detections: {0}. Action taken: Added to IP set and queue.'.
                        format(len(alb_client_http_flood_critical_list)))
        else:
            LOGGER.info('Critical level flood detections: 0.')

        LOGGER.info('--------------------------- [Attacker information] ---------------------------')

        LOGGER.info('Low level flood detections [{0}]: '.format(len(alb_client_http_flood_low_list)))

        if alb_client_http_flood_low_list:
            for alb_client in alb_client_http_flood_low_list:
                LOGGER.info('\t - Client IP: {0}. Number of requests: {1}'
                            .format(alb_client.client_ip, alb_client.number_of_requests))
        else:
            LOGGER.info('None.')

        LOGGER.info('Medium level flood detections [{0}]: '.format(len(alb_client_http_flood_medium_list)))

        if alb_client_http_flood_medium_list:
            for alb_client in alb_client_http_flood_medium_list:
                LOGGER.info('Client IP: {0}. Number of requests: {1}'
                            .format(alb_client.client_ip, alb_client.number_of_requests))
        else:
            LOGGER.info('None.')

        LOGGER.info('Critical level flood detections [{0}]: '.format(len(alb_client_http_flood_critical_list)))

        if alb_client_http_flood_critical_list:
            for alb_client in alb_client_http_flood_critical_list:
                LOGGER.info('Client IP: {0}. Number of requests: {1}'
                            .format(alb_client.client_ip, alb_client.number_of_requests))
        else:
            LOGGER.info('None.')
