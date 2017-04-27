import connexion
from swagger_server.models.error import Error
from swagger_server.models.station import Station
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from routes_aggregator.service import Service
from routes_aggregator.exceptions import ApplicationException


def convert_station(model_station, language):
    if model_station:
        return Station(
            model_station.domain_id,
            model_station.agent_type,
            model_station.get_station_name(language),
            model_station.get_country_name(language)
        )
    else:
        return None


def find_stations_get(station_name, language, search_mode=None, limit=None):
    """
    Find stations by name.
    
    :param station_name: 
    :type station_name: str
    :param language: 
    :type language: str
    :param search_mode: 
    :type search_mode: str
    :param limit: 
    :type limit: int

    :rtype: List[Station]
    """

    try:
        model_stations = Service().find_stations(
            station_name, language, search_mode, limit
        )

        return list(
            map(
                lambda model_station: convert_station(model_station, language),
                model_stations
            )
        )
    except ApplicationException as e:
        return Error(0, str(e))


def get_station_get(station_id, language):
    """
    Get station by identifier.
    
    :param station_id: 
    :type station_id: str
    :param language: 
    :type language: str

    :rtype: Station
    """

    try:
        return convert_station(
            Service().get_station(station_id, language), language
        )
    except ApplicationException as e:
        return Error(0, str(e))
