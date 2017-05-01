import connexion
from swagger_server.models.error import Error
from swagger_server.models.route import Route
from swagger_server.models.route_point import RoutePoint
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from routes_aggregator.service import Service
from routes_aggregator.exceptions import ApplicationException
from routes_aggregator.model import Route as ModelRoute, Station as ModelStation, Entity


def convert_route_point(model_point, agent_type):
    return RoutePoint(
        route_id=ModelRoute.get_domain_id(agent_type, model_point.route_id),
        station_id=ModelStation.get_domain_id(agent_type, model_point.station_id),
        arrival_time=model_point.arrival_time,
        departure_time=model_point.departure_time,
        stop_time=model_point.stop_time
    )


def convert_route(model_route, language):
    if model_route:
        return Route(
            route_id=model_route.domain_id,
            agent_type=model_route.agent_type,
            route_number=model_route.route_number,
            departure_station_id=ModelStation.get_domain_id(model_route.agent_type, model_route.departure_point.station_id),
            departure_time=model_route.departure_time,
            arrival_station_id=ModelStation.get_domain_id(model_route.agent_type, model_route.arrival_point.station_id),
            arrival_time=model_route.arrival_time,
            travel_time=model_route.travel_time,
            periodicity=Entity.extract_property(model_route.get_periodicity, language),
            route_points=list(
                map(
                    lambda model_point: convert_route_point(
                        model_point, model_route.agent_type
                    ),
                    model_route.route_points
                )
            )
        )
    else:
        return None


def find_routes_get(language, route_number=None, station_ids=None, search_mode=None, limit=None):
    """
    Find routes by number or by station identifiers.
    
    :param language: 
    :type language: str
    :param route_number: 
    :type route_number: str
    :param station_ids: 
    :type station_ids: List[str]
    :param search_mode: 
    :type search_mode: str
    :param limit: 
    :type limit: int

    :rtype: List[Route]
    """

    try:
        model_routes = Service().find_routes(
            language, route_number, station_ids, search_mode, limit
        )
        return list(
            map(
                lambda model_station: convert_route(model_station, language),
                model_routes
            )
        )
    except ApplicationException as e:
        return Error(0, str(e))


def get_route_get(route_id, language):
    """
    Get route by identifier.
    
    :param route_id: 
    :type route_id: str
    :param language: 
    :type language: str

    :rtype: Route
    """

    try:
        return convert_route(
            Service().get_route(route_id, language), language
        )
    except ApplicationException as e:
        return Error(0, str(e))
