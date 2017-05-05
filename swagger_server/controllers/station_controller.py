import connexion
from swagger_server.models.error import Error
from swagger_server.models.station import Station
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import swagger_server.controllers.basic_controller as controller


def find_stations_get(station_names, language, search_mode=None, limit=None):
    """
    Find stations by name.

    :param station_names: 
    :type station_names: List[str]
    :param language: 
    :type language: str
    :param search_mode: 
    :type search_mode: str
    :param limit: 
    :type limit: int

    :rtype: List[Station]
    """

    return controller.find_stations_get(station_names, language, search_mode, limit)


def get_station_get(station_id, language):
    """
    Get station by identifier.
    
    :param station_id: 
    :type station_id: str
    :param language: 
    :type language: str

    :rtype: Station
    """

    return controller.get_station_get(station_id, language)
