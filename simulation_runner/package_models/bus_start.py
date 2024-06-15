from datetime import datetime
import logging
from FinalProjectSimulator.simulation_runner.package_models.event import Event


logger = logging.getLogger(__name__)


class BusStart(Event):
    def __init__(self, simulation_manager, time: datetime, bus: "Bus"):
        super().__init__(simulation_manager, time)
        self.bus = bus

    def handle(self) -> bool:
        logger.debug("started")
        logger.info("Event time: %s Type: BusStart for bus %d", self.time.isoformat(), self.bus.id)
        # TODO: implement handler

        logger.debug("finished")
        pass


from FinalProjectSimulator.simulation_runner.package_models.bus import Bus
