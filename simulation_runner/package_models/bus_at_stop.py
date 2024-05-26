from datetime import datetime
from .event import Event
import logging


logger = logging.getLogger(__name__)


class BusAtStop(Event):
    def __init__(
        self, simulation_manager: "SimulationManager", time: datetime, bus: "Bus", stop: "Stop"
    ):
        super().__init__(simulation_manager, time)
        self.bus = bus
        self.stop = stop

    def handle(self) -> bool:
        logger.debug("started")
        logger.info(
            "Handling BusAtStop event for bus %d at stop %d",
            self.bus.id,
            self.stop.id,
        )
        # TODO: implement handler

        logger.debug("finished")
        pass


from .bus import Bus
from .stop import Stop
from ..simulation_manager import SimulationManager
