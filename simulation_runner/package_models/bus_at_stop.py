from datetime import datetime
import logging
from FinalProjectSimulator.simulation_runner.package_models.event import Event


logger = logging.getLogger(__name__)


class BusAtStop(Event):
    def __init__(
        self, simulation_manager, time: datetime, bus: "Bus", stop: "Stop"
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


from FinalProjectSimulator.simulation_runner.package_models.bus import Bus
from FinalProjectSimulator.simulation_runner.package_models.stop import Stop
