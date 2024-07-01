from datetime import datetime, timedelta
import logging
from FinalProjectSimulator.data_repo.analyzed_lines import get_green_stations
from FinalProjectSimulator.data_repo.gtfs import get_stop_codes_and_arrival_times, get_stop_location, get_trip_ids_and_departure_times
from FinalProjectSimulator.data_repo.ridership import get_all_stations
from FinalProjectSimulator.models.simulation import Simulation
from FinalProjectSimulator.simulation_runner.package_models.express_bus import Bus, ExpressBus
from FinalProjectSimulator.simulation_runner.package_models.stop import Stop
from FinalProjectSimulator.utilities.gmaps import get_route_timedeltas, get_route


logger = logging.getLogger(__name__)


class RouteManager:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
        self.stops: list[Stop] = []
        self.general_route: list[tuple[Stop, timedelta]] = None

    def create_stops(self) -> list[Stop]:
        logger.debug("started")
        logger.info("Creating stops")
        ridership_df = get_all_stations(self.simulation.line_id)
        for _, row in ridership_df.iterrows():
            stop_location = get_stop_location(row["תחנה"])
            stop = Stop(row["תחנה"], row["סידורי תחנה"],
                        row["שם תחנה"], stop_location)
            self.stops.append(stop)
        self.stops.sort(key=lambda x: x.ordinal_number)
        logger.debug("finished")
        return self.stops

    def create_route(self, bus: Bus) -> list[tuple[Stop, datetime]]:
        logger.debug("started")
        logger.info("Creating route for bus %d", bus.id)

        stop_codes_and_times = get_stop_codes_and_arrival_times(bus.id)        
        route = self.__create_route_as_timedeltas(stop_codes_and_times)
        route = self.__convert_route_to_datetimes(bus.leave_time, route)
        
        if len(route) == 0:
            logger.warning(f"Route for bus with trip id {bus.id} is empty. Will create based on general route")
            if self.general_route is None:
                self.__create_general_route()
            route = self.__convert_route_to_datetimes(bus.leave_time, self.general_route)        

        logger.debug("finished")
        return route

    def create_initial_express_route(self, bus: Bus) -> list[tuple[Stop, datetime, bool]]:
        logger.debug("started")
        logger.info("Creating express route for bus %d", bus.id)

        green_stations = get_green_stations(
            self.simulation.line_id, bus.leave_time)
        express_stops: list[Stop] = [self.stops[0]]  # Start with the first stop
        for stop_code, stop_sequence in green_stations.itertuples(index=False):
            stop = next(
                (stop for stop in self.stops if stop.ordinal_number == stop_sequence), None)
            if stop is None:
                logger.error(
                    "Stop with code %s not found in simulation stops", stop_code)
                return []
            if stop not in express_stops:
                express_stops.append(stop)
        # Add the last stop
        if express_stops[-1].ordinal_number != self.stops[-1].ordinal_number:
            express_stops.append(self.stops[-1])
        express_stops.sort(key=lambda x: x.ordinal_number)
        stops_locations = [stop.location for stop in express_stops]
        stops_datetimes = get_route(bus.leave_time, stops_locations)
        # Create a dictionary to map express stops to their times
        express_stops_times = {
            express_stops[i].ordinal_number: stops_datetimes[i] for i in range(len(express_stops))}

        route: list[tuple[Stop, datetime, bool]] = []
        last_arrival_time = None

        for stop in self.stops:
            if stop.ordinal_number in express_stops_times:
                last_arrival_time = express_stops_times[stop.ordinal_number]
                route.append((stop, last_arrival_time, True))
            else:
                route.append((stop, last_arrival_time, False))

        logger.debug("finished")
        return route
    
    def create_express_route(self, bus: ExpressBus) -> list[tuple[Stop, datetime]]:
        bus.pending_stops.sort(key=lambda x: x.ordinal_number)
        stops_locations = [stop.location for stop in bus.pending_stops]
        stops_datetimes = get_route(bus.leave_time, stops_locations)
        route = list(zip(bus.pending_stops, stops_datetimes))
        return route

    def earliest_bus_arriving_stop(self, buses: list["Bus"], stop: "Stop") -> "Bus":
        earliest_bus = None
        earliest_time = None

        for bus in buses:
            arrival_time = next(
                (
                    arrival_time
                    for bus_stop, arrival_time in bus.route
                    if bus_stop == stop
                ),
                None,
            )
            if arrival_time is not None and (earliest_time is None or arrival_time < earliest_time):
                earliest_time = arrival_time
                earliest_bus = bus

        return earliest_bus
        
    def __create_general_route(self) -> list[tuple[Stop, timedelta]]:
        logger.debug("started")
        logger.info("Creating general route for line %s", self.simulation.line_id)
        
        trip_ids = get_trip_ids_and_departure_times(self.simulation.line_id, self.simulation.start_time)
        for trip_id in trip_ids["TripId"]:
            stops_and_arrival_times = get_stop_codes_and_arrival_times(trip_id)
            if stops_and_arrival_times.empty or stops_and_arrival_times.shape[0] == 0:
                continue
            general_route = self.__create_route_as_timedeltas(stops_and_arrival_times)
            if len(general_route) > 0:
                self.general_route = general_route
                break
        
        logger.debug("finished")
        return general_route
    
    def __create_route_as_timedeltas(self, stop_codes_and_times) -> list[tuple[Stop, timedelta]]:
        logger.debug("started")
        route: list[tuple[Stop, timedelta]] = []
        
        last_arrival_time = None
        for stop_code, arrival_time in stop_codes_and_times.itertuples(index=False):
            if last_arrival_time is None: # for first iteration
                last_arrival_time = arrival_time
                
            stop = next(
                (stop for stop in self.stops if stop.id == stop_code), None)
            if stop is None:
                logger.error(
                    "Stop with code %s not found in simulation stops", stop_code)
                return []
            
            time_between_stops = arrival_time - last_arrival_time
            route.append((stop, time_between_stops))
            last_arrival_time = arrival_time
            
        route.sort(key=lambda x: x[0].ordinal_number)
        
        logger.debug("finished")
        return route
        
    def __convert_route_to_datetimes(self, leave_time: datetime, route: list[tuple[Stop, timedelta]]) -> list[tuple[Stop, datetime]]:
        logger.debug("started")
        
        new_route: list[tuple[Stop, datetime]] = []
        last_arrival_time = leave_time
        for stop, time in route:
            arrival_time = last_arrival_time + time
            new_route.append((stop, arrival_time))
            last_arrival_time = arrival_time
            
        logger.debug("finished")
        return new_route
    