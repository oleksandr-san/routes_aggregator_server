# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.error import Error
from swagger_server.models.path import Path
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestPathController(BaseTestCase):
    """ PathController integration test stubs """

    def test_find_paths_get(self):
        """
        Test case for find_paths_get

        Find paths between stations.
        """
        query_string = [('station_ids', 'station_ids_example'),
                        ('search_mode', 'simple'),
                        ('max_transitions_count', 4),
                        ('limit', 16)]
        response = self.client.open('/v1/find_paths',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
