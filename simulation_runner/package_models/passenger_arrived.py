from datetime import datetime
import logging
from FinalProjectSimulator.simulation_runner.package_models.event import Event
from FinalProjectSimulator.simulation_runner.package_models.passenger import Passenger


logger = logging.getLogger(__name__)


class PassengerArrived(Event):
    def __init__(self, simulation_manager: "SimulationManager", time: datetime, passenger: Passenger):
        super().__init__(simulation_manager, time)
        self.passenger = passenger

    def handle(self) -> bool:
        logger.debug("started")
        logger.info(
            "Event time: %s Type: PassengerArrived for passenger %d", self.time.isoformat(), self.passenger.id)
        if self.passenger.stop_src.add_passenger(self.passenger) is False:
            logger.error("Failed to add passenger %d to stop %d",
                         self.passenger.id, self.passenger.stop_src.id)
            return False
        logger.debug("finished")
        return True


from FinalProjectSimulator.simulation_runner.simulation_manager import SimulationManager
