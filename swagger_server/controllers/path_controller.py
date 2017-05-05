import connexion
from swagger_server.models.error import Error
from swagger_server.models.path import Path
from swagger_server.models.path_item import PathItem
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import swagger_server.controllers.basic_controller as controller


def find_paths_get(station_ids, language, search_mode=None, max_transitions_count=None, limit=None):
    """
    Find paths between stations.

    :param station_ids: 
    :type station_ids: List[str]
    :param language: 
    :type language: str
    :param search_mode: 
    :type search_mode: str
    :param max_transitions_count: 
    :type max_transitions_count: int
    :param limit: 
    :type limit: int

    :rtype: List[Path]
    """

    return controller.find_paths_get(
        station_ids=station_ids, language=language,
        search_mode=search_mode, max_transitions_count=max_transitions_count,
        limit=limit
    )
