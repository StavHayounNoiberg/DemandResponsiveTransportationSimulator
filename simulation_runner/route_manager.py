from datetime import datetime
import logging
from FinalProjectSimulator.data_repo.ridership import fetch_all_stations
from FinalProjectSimulator.models.simulation import Simulation
from FinalProjectSimulator.simulation_runner.package_models.bus import Bus
from FinalProjectSimulator.simulation_runner.package_models.stop import Stop


logger = logging.getLogger(__name__)


class RouteManager:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
        self.stops: list[Stop] = []

    def create_stops(self) -> list[Stop]:
        logger.debug("started")
        logger.info("Creating stops")
        ridership_df = fetch_all_stations(self.simulation.line_id)
        for index, row in ridership_df.iterrows():
            stop = Stop(row["תחנה"], row["סידורי תחנה"], row["שם תחנה"])
            self.stops.append(stop)
        self.stops.sort(key=lambda x: x.ordinal_number)
        logger.debug("finished")
        return self.stops

    def create_route(self, bus: Bus) -> list[tuple[Stop, datetime]]:
        logger.debug("started")
        logger.info("Creating route for bus %d", bus.id)
        # TODO: 1. Updates the route of the bus with the list of stops and arrival times by using "update_route"
        # 2. Updates each stop's buses list with the bus and the arrival time by using "add_bus"

        logger.debug("finished")
        pass

    def create_express_route(self, bus: Bus) -> list[tuple[Stop, datetime]]:
        logger.debug("started")
        logger.info("Creating express route for bus %d", bus.id)
        # TODO: Think how to do this. At the end should updates each stop's buses list with the bus and the arrival time by using "add_bus"

        logger.debug("finished")
        pass
