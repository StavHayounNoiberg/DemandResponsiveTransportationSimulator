import logging
from ..models.simulation import Simulation
from .package_models.bus import Bus
from .package_models.stop import Stop


logger = logging.getLogger(__name__)


class LineManager:
    def __init__(self, simulation: Simulation):
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

    def find_next_express_bus(self, stop: Stop) -> Bus:
        logger.debug("started")
        logger.info("Finding next express bus for stop %d", stop.id)
        # TODO: Implement this method

        logger.debug("finished")
        pass
