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
        # TODO: 1. Creates all buses for the entire simulation time
        # 2. Defines for each bus if it’s an express bus or ordinary
        # 3. For each ordinary bus: calls "create_route"

        logger.debug("finished")
        pass

    def find_next_express_bus(self, stop: Stop) -> "Bus":
        logger.debug("started")
        logger.info("Finding next express bus for stop %d", stop.id)
        # TODO: Implement this method

        logger.debug("finished")
        pass


from FinalProjectSimulator.simulation_runner.package_models.bus import Bus
from FinalProjectSimulator.simulation_runner.package_models.express_bus import ExpressBus