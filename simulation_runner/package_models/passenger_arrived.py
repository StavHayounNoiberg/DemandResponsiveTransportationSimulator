from datetime import datetime
import logging
from .event import Event
from .passenger import Passenger


logger = logging.getLogger(__name__)


class PassengerArrived(Event):
    def __init__(self, simulation_manager: "SimulationManager", time: datetime, passenger: Passenger):
        super().__init__(simulation_manager, time)
        self.passenger = passenger

    def handle(self) -> bool:
        logger.debug("started")
        logger.info(
            "Handling PassengerArrived event for passenger %d", self.passenger.id
        )
        # TODO: implement handler

        logger.debug("finished")
        pass


from ..simulation_manager import SimulationManager
