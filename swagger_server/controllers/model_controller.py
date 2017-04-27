import connexion
from swagger_server.models.error import Error
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from routes_aggregator.service import Service
from routes_aggregator.exceptions import ApplicationException


def request_model_update_get(agent_type, build_model=None):
    """
    Request model update.
    
    :param agent_type: 
    :type agent_type: str
    :param build_model: 
    :type build_model: bool

    :rtype: str
    """

    try:
        Service().request_model_update(agent_type, build_model)
    except ApplicationException as e:
        return Error(0, str(e))