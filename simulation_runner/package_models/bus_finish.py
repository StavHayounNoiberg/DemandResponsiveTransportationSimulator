from datetime import datetime
import logging
from FinalProjectSimulator.simulation_runner.package_models.event import Event


logger = logging.getLogger(__name__)


class BusFinish(Event):
    def __init__(self, simulation_manager: "SimulationManager", time: datetime, bus: "Bus"):
        super().__init__(simulation_manager, time)
        self.bus = bus

    def handle(self) -> bool:
        logger.debug("started")
        logger.info("Event time: %s Type: BusFinish for bus %d", self.time.isoformat(), self.bus.id)
        
        # validating that no passengers left on the bus
        if len(self.bus.passengers) > 0:
            logger.error("Bus %d has passengers left on it", self.bus.id)
            raise Exception("Bus %d has passengers left on it", self.bus.id)
        
        logger.debug("finished")
        return True


from FinalProjectSimulator.simulation_runner.package_models.bus import Bus
from FinalProjectSimulator.simulation_runner.simulation_manager import SimulationManager
