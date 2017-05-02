import connexion
from swagger_server.models.error import Error
from swagger_server.models.path import Path
from swagger_server.models.path_item import PathItem
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from routes_aggregator.service import Service
from routes_aggregator.exceptions import ApplicationException


def convert_array(array):
    result = []
    for item in array:
        if item == -1 or item == '-1':
            result.append([])
        else:
            if not result:
                result.append([])
            result[-1].append(item)
    return result


def convert_path_item(model_item):
    return PathItem(
        route_id=model_item.route.domain_id,
        departure_point_idx=model_item.departure_point_idx,
        arrival_point_idx=model_item.arrival_point_idx,
        departure_time=model_item.departure_time,
        arrival_time=model_item.arrival_time,
        travel_time=model_item.travel_time
    )


def convert_path(model_path):
    if model_path:
        return Path(
            departure_station_id=model_path.departure_station_id,
            arrival_station_id=model_path.arrival_station_id,
            departure_time=model_path.departure_time,
            arrival_time=model_path.arrival_time,
            travel_time=model_path.travel_time,
            raw_travel_time=model_path.row_travel_time,
            path_items=list(
                map(convert_path_item, model_path.path_items)
            )
        )
    else:
        return None


def find_paths_get(station_ids, search_mode=None,
                   use_strict_intermediate_stations=None,
                   max_transitions_count=None, limit=None):
    """
    Find paths between stations.

    :param station_ids: 
    :type station_ids: List[]
    :param search_mode: 
    :type search_mode: str
    :param use_strict_intermediate_stations: 
    :type use_strict_intermediate_stations: bool
    :param max_transitions_count: 
    :type max_transitions_count: int
    :param limit: 
    :type limit: int

    :rtype: List[Path]
    """

    try:
        model_paths = Service().find_paths(
            station_ids=convert_array(station_ids), search_mode=search_mode,
            use_strict_intermediate_stations=use_strict_intermediate_stations,
            max_transitions_count=max_transitions_count, limit=limit
        )

        return list(
            map(
                lambda model_path: convert_path(model_path),
                model_paths
            )
        )
    except ApplicationException as e:
        return Error(0, str(e))
