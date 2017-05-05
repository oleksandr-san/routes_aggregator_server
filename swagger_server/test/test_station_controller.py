# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.error import Error
from swagger_server.models.station import Station
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestStationController(BaseTestCase):
    """ StationController integration test stubs """

    def test_find_stations_get(self):
        """
        Test case for find_stations_get

        Find stations by name.
        """
        query_string = [('station_names', 'station_names_example'),
                        ('search_mode', 'starts_with'),
                        ('language', 'language_example'),
                        ('limit', 16)]
        response = self.client.open('/v1/find_stations',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_station_get(self):
        """
        Test case for get_station_get

        Get station by identifier.
        """
        query_string = [('station_id', 'station_id_example'),
                        ('language', 'language_example')]
        response = self.client.open('/v1/get_station',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
