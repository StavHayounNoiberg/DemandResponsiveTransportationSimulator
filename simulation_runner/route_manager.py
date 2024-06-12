from datetime import datetime
import logging
from FinalProjectSimulator.data_repo.analyzed_lines import get_green_stations
from FinalProjectSimulator.data_repo.gtfs import get_stop_codes_and_arrival_times, get_stop_location
from FinalProjectSimulator.data_repo.ridership import get_all_stations
from FinalProjectSimulator.models.simulation import Simulation
from FinalProjectSimulator.simulation_runner.package_models.bus import Bus
from FinalProjectSimulator.simulation_runner.package_models.stop import Stop
from FinalProjectSimulator.utilities.gmaps import get_route


logger = logging.getLogger(__name__)


class RouteManager:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
        self.stops: list[Stop] = []

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
        route: list[tuple[Stop, datetime]] = []

        for stop_code, arrival_time in stop_codes_and_times.itertuples(index=False):
            stop = next(
                (stop for stop in self.stops if stop.id == stop_code), None)
            if stop is None:
                logger.error(
                    "Stop with code %s not found in simulation stops", stop_code)
                return []
            arrival_datetime = datetime.combine(
                bus.leave_time.date(), (datetime.min + arrival_time).time())
            route.append((stop, arrival_datetime))

        route.sort(key=lambda x: x[1])
        logger.debug("finished")
        return route

    def create_express_route(self, bus: Bus) -> list[tuple[Stop, datetime, bool]]:
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
            express_stops.append(stop)
        # Add the last stop
        if express_stops[-1].ordinal_number != self.stops[-1].ordinal_number:
            express_stops.append(self.stops[-1])
        express_stops.sort(key=lambda x: x.ordinal_number)
        express_stops_time = get_route(bus.leave_time, express_stops)
        # Create a dictionary to map express stops to their times
        express_stop_times = {
            express_stops[i].ordinal_number: express_stops_time[i] for i in range(len(express_stops))}

        route: list[tuple[Stop, datetime, bool]] = []
        last_arrival_time = None

        for stop in self.stops:
            if stop.ordinal_number in express_stop_times:
                last_arrival_time = express_stop_times[stop.ordinal_number]
                route.append((stop, last_arrival_time, True))
            else:
                route.append((stop, last_arrival_time, False))

        logger.debug("finished")
        return route

    def earliest_bus_arriving_stop(buses: list["Bus"], stop: "Stop") -> "Bus":
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
            if earliest_time is None or arrival_time < earliest_time:
                earliest_time = arrival_time
                earliest_bus = bus

        return earliest_bus
