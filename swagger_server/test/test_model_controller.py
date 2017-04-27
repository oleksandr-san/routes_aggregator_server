# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.error import Error
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestModelController(BaseTestCase):
    """ ModelController integration test stubs """

    def test_request_model_update_get(self):
        """
        Test case for request_model_update_get

        Request model update.
        """
        query_string = [('agent_type', 'agent_type_example'),
                        ('build_model', false)]
        response = self.client.open('/v1/request_model_update',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
