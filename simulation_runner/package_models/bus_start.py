from datetime import datetime
import logging
from .event import Event


logger = logging.getLogger(__name__)


class BusStart(Event):
    def __init__(self, simulation_manager: "SimulationManager", time: datetime, bus: "Bus"):
        super().__init__(simulation_manager)
        self.bus = bus

    def handle(self) -> bool:
        logger.debug("started")
        logger.info("Handling BusStart event for bus %d", self.bus.id)
        # TODO: implement handler

        logger.debug("finished")
        pass


from .bus import Bus
from ..simulation_manager import SimulationManager
