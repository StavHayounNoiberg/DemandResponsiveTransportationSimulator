from datetime import datetime
import logging
import numpy as np
from FinalProjectSimulator.data_repo.gtfs import get_trip_ids_and_departure_times
from FinalProjectSimulator.models.simulation import Simulation
from FinalProjectSimulator.simulation_runner.package_models.stop import Stop
from FinalProjectSimulator.utilities.datetime_utils import get_datetimes_between


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
            gtfs_data = get_trip_ids_and_departure_times(self.simulation.line_id, date)
            for trip_id, departure_time in gtfs_data.itertuples(index=False):
                if departure_time > self.simulation.end_time:
                    continue
                bus, bus_stops = None, None
                is_express = np.random.choice([True, False], p=[self.simulation.express_rate, 1 - self.simulation.express_rate])
                if is_express:
                    bus = ExpressBus(trip_id, self, departure_time)
                    bus_stops = (self.simulation_manager.route_manager.create_initial_express_route(bus))
                    pending_stops = [stop for stop, _, is_green in bus_stops if is_green]
                    if bus.set_pending_stops(pending_stops) is False:
                        logger.error("Failed to set pending stops for express bus %d", bus.id)
                        return []
                    bus_route = [(stop, time) for stop, time, _ in bus_stops]
                    if bus.update_route(bus_route) is False:
                        logger.error("Failed to update route for express bus %d", self.id)
                        return []
                    
                    # TODO: Check performance and decide if to use approximate route
                    # approximate_route = self.simulation_manager.route_manager.get_approximate_route()
                    # bus_stops = [(stop, departure_time + time) for stop, time in approximate_route]
                else:
                    bus = Bus(trip_id, self, departure_time)
                    bus_stops = self.simulation_manager.route_manager.create_route(bus)
                    if bus.update_route(bus_stops) is False:
                        logger.error("Failed to update route for bus %d", bus.id)
                        return []
                
                if bus.update_last_next_stop() is False:
                    logger.error("Failed to update last and next stop for bus %d", bus.id)
                    return []

                for stop in bus_stops:
                    stop[0].add_bus(bus, stop[1])
                self.buses.append(bus)

        logger.debug("finished")
        self.buses.sort(key=lambda x: x.leave_time)
        return self.buses

    def find_next_express_bus(self, stop: Stop, desired_time: datetime) -> "Bus":
        logger.debug("started")
        logger.info("Finding next express bus for stop %d", stop.id)

        next_bus = next(
            (bus for bus in self.buses 
            if type(bus) is ExpressBus 
            and bus.next_stop is not None 
            and bus.next_stop.ordinal_number <= stop.ordinal_number 
            and any(route_stop == stop and arrival_time >= desired_time for route_stop, arrival_time in bus.route)), 
            None
        )
        
        if next_bus is None:
            logger.warning("No express bus found for stop %d", stop.id)
            return None

        logger.debug("finished")
        return next_bus


from FinalProjectSimulator.simulation_runner.package_models.express_bus import ExpressBus
from FinalProjectSimulator.simulation_runner.package_models.bus import Bus
