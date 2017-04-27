# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.error import Error
from swagger_server.models.route import Route
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestRouteController(BaseTestCase):
    """ RouteController integration test stubs """

    def test_find_routes_get(self):
        """
        Test case for find_routes_get

        Find routes by number or by station identifiers.
        """
        query_string = [('route_number', 'route_number_example'),
                        ('station_ids', 'station_ids_example'),
                        ('language', 'language_example'),
                        ('search_mode', 'starts_with'),
                        ('limit', 16)]
        response = self.client.open('/v1/find_routes',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_route_get(self):
        """
        Test case for get_route_get

        Get route by identifier.
        """
        query_string = [('route_id', 'route_id_example'),
                        ('language', 'language_example')]
        response = self.client.open('/v1/get_route',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
