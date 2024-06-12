from datetime import datetime
import logging
import numpy as np
from FinalProjectSimulator.data_repo.gtfs import get_trip_ids_and_departure_times
from FinalProjectSimulator.models.simulation import Simulation
from FinalProjectSimulator.simulation_runner.package_models.stop import Stop
from FinalProjectSimulator.utilities.datetime_utils import get_day_number, get_datetimes_between


logger = logging.getLogger(__name__)


class LineManager:
    def __init__(self, simulation_manager, simulation: Simulation):
        self.simulation_manager = simulation_manager
        self.simulation = simulation
        self.buses: list["Bus"] = []

    def create_buses(self) -> list["Bus"]:
        logger.debug("started")
        logger.info("Creating buses")

        date_list = get_datetimes_between(
            self.simulation.start_time, self.simulation.end_time)
        
        for date in date_list:
            gtfs_data = get_trip_ids_and_departure_times(
                self.simulation.line_id, date)
            for trip_id, departure_time in gtfs_data.itertuples(index=False):
                bus, bus_stops = None, None
                is_express = np.random.choice([True, False], p=[
                                              self.simulation.express_rate, 1 - self.simulation.express_rate])
                if is_express:
                    bus = ExpressBus(trip_id, self, departure_time)
                    bus_stops = (
                        self.simulation_manager.route_manager.create_express_route(bus))
                else:
                    bus = Bus(trip_id, self, departure_time)
                    bus_stops = self.simulation_manager.route_manager.create_route(
                        bus)

                if bus.update_route(bus_stops) is False:
                    logger.error("Failed to update route for bus %d", bus.id)
                    return []

                for stop in bus_stops:
                    stop[0].add_bus(bus, stop[1])
                self.buses.append(bus)

        logger.debug("finished")
        return self.buses

    def find_next_express_bus(self, stop: Stop, desired_time: datetime) -> "Bus":
        logger.debug("started")
        logger.info("Finding next express bus for stop %d", stop.id)

        next_bus = next((bus for bus in self.buses if type(
            bus) is ExpressBus and bus.next_stop.ordinal_number is not None and bus.next_stop.ordinal_number <= stop.ordinal_number), None)
        if next_bus is None:
            logger.warning("No express bus found for stop %d", stop.id)
            return None

        logger.debug("finished")
        return next_bus


from FinalProjectSimulator.simulation_runner.package_models.express_bus import ExpressBus
from FinalProjectSimulator.simulation_runner.package_models.bus import Bus
