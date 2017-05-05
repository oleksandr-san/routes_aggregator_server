from swagger_server.models.error import Error
from swagger_server.models.path import Path
from swagger_server.models.path_item import PathItem
from swagger_server.models.route import Route
from swagger_server.models.route_point import RoutePoint
from swagger_server.models.station import Station

from routes_aggregator.service import Service
from routes_aggregator.exceptions import ApplicationException

from routes_aggregator.model import \
    Station as ModelStation, \
    Entity as ModelEntity

service = Service()


def shielded_execute(executor):
    def shielded_executor(*args, **kwargs):
        try:
            return executor(*args, **kwargs)
        except ApplicationException as e:
            return Error(0, str(e))
    return shielded_executor


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


def convert_station(model_station, language):
    if not model_station:
        return None

    return Station(
        id=model_station.domain_id,
        agent_type=model_station.agent_type,
        station_name=ModelEntity.extract_property(model_station.get_station_name, language),
        country_name=ModelEntity.extract_property(model_station.get_country_name, language)
    )


def convert_route_point(model_point, agent_type, language):
    if not model_point:
        return None

    station_id = ModelStation.get_domain_id(agent_type, model_point.station_id)

    return RoutePoint(
        station=convert_station(service.get_station(station_id), language),
        arrival_time=model_point.arrival_time,
        departure_time=model_point.departure_time,
        stop_time=model_point.stop_time
    )


def convert_route(model_route, language, collect_points):
    if not model_route:
        return None

    departure_station_id = ModelStation.get_domain_id(
        model_route.agent_type, model_route.departure_point.station_id)

    arrival_station_id = ModelStation.get_domain_id(
        model_route.agent_type, model_route.arrival_point.station_id)

    route_points = []
    if collect_points:
        route_points.extend(
            map(
                lambda model_point: convert_route_point(
                    model_point, model_route.agent_type, language
                ),
                model_route.route_points
            )
        )

    return Route(
        id=model_route.domain_id,
        agent_type=model_route.agent_type,
        route_number=model_route.route_number,
        departure_station=convert_station(service.get_station(departure_station_id), language),
        departure_time=model_route.departure_time,
        arrival_station=convert_station(service.get_station(arrival_station_id), language),
        arrival_time=model_route.arrival_time,
        travel_time=model_route.travel_time,
        periodicity=ModelEntity.extract_property(model_route.get_periodicity, language),
        route_points=route_points
    )


def convert_path_item(model_item, language):
    if not model_item:
        return None

    departure_station_id = model_item.departure_point.station_id
    arrival_station_id = model_item.arrival_point.station_id

    route_points = list(
        map(
            lambda model_point: convert_route_point(
                model_point,
                model_item.route.agent_type,
                language
            ),
            model_item.browse_route_points()
        )
    )

    return PathItem(
        route_number=model_item.route.route_number,
        departure_station=convert_station(service.get_station(departure_station_id), language),
        departure_time=model_item.departure_time,
        arrival_station=convert_station(service.get_station(arrival_station_id), language),
        arrival_time=model_item.arrival_time,
        travel_time=model_item.travel_time,
        route_points=route_points
    )


def convert_path(model_path, language):
    if not model_path:
        return None

    departure_station_id = model_path.departure_station_id
    arrival_station_id = model_path.arrival_station_id

    path_items = list(
        map(
            lambda model_item: convert_path_item(model_item, language),
            model_path.path_items
        )
    )

    return Path(
        departure_station=convert_station(service.get_station(departure_station_id), language),
        departure_time=model_path.departure_time,
        arrival_station=convert_station(service.get_station(arrival_station_id), language),
        arrival_time=model_path.arrival_time,
        travel_time=model_path.travel_time,
        path_items=path_items
    )


@shielded_execute
def get_station_get(station_id, language):
    return convert_station(
        service.get_station(station_id), language
    )


@shielded_execute
def find_stations_get(station_names, language, search_mode=None, limit=None):
    model_stations = service.find_stations(
        station_names=station_names, search_mode=search_mode, limit=limit
    )

    return list(
        map(
            lambda model_station: convert_station(model_station, language),
            model_stations
        )
    )


@shielded_execute
def get_route_get(route_id, language):
    return convert_route(service.get_route(route_id), language, True)


@shielded_execute
def find_routes_get(language,
                    route_numbers=None, station_ids=None,
                    search_mode=None, collect_points=None, limit=None):

    model_routes = service.find_routes(
        route_numbers=route_numbers, station_ids=station_ids,
        search_mode=search_mode, limit=limit
    )

    return list(
        map(
            lambda model_station: convert_route(model_station, language, collect_points),
            model_routes
        )
    )


@shielded_execute
def find_paths_get(station_ids, language,
                   search_mode=None, max_transitions_count=None, limit=None):

    model_paths = service.find_paths(
        station_ids=convert_array(station_ids), search_mode=search_mode,
        max_transitions_count=max_transitions_count, limit=limit
    )

    return list(
        map(
            lambda model_path: convert_path(model_path, language),
            model_paths
        )
    )
