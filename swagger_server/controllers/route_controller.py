import connexion
from swagger_server.models.error import Error
from swagger_server.models.route import Route
from swagger_server.models.route_point import RoutePoint
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import swagger_server.controllers.basic_controller as controller


def find_routes_get(language, route_numbers=None,
                    station_ids=None, search_mode=None,
                    collect_points=None, limit=None):
    """
    Find routes by number or by station identifiers.

    :param language: 
    :type language: str
    :param route_numbers: 
    :type route_numbers: List[str]
    :param station_ids: 
    :type station_ids: List[str]
    :param search_mode: 
    :type search_mode: str
    :param collect_points: 
    :type collect_points: bool
    :param limit: 
    :type limit: int

    :rtype: List[Route]
    """

    return controller.find_routes_get(
        language=language, route_numbers=route_numbers,
        station_ids=station_ids, search_mode=search_mode,
        collect_points=collect_points, limit=limit
    )


def get_route_get(route_id, language):
    """
    Get route by identifier.
    
    :param route_id: 
    :type route_id: str
    :param language: 
    :type language: str

    :rtype: Route
    """

    return controller.get_route_get(route_id=route_id, language=language)