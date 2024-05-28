from datetime import datetime
import logging
from FinalProjectSimulator.simulation_runner.package_models.event import Event


logger = logging.getLogger(__name__)


class PassengerRequest(Event):
    def __init__(
        self,
        simulation_manager: "SimulationManager",
        time: datetime,
        line_id: str,
        stop_src: str,
        stop_dest: str,
        is_reporting: bool,
        leaving_time: datetime,
    ):
        super().__init__(simulation_manager, time)
        self.line_id = line_id
        self.stop_src = stop_src
        self.stop_dest = stop_dest
        self.is_reporting = is_reporting
        self.leaving_time = leaving_time

    def handle(self) -> bool:
        logger.debug("started")
        logger.info(
            "Handling PassengerRequest event for passenger %d", self.passenger.id
        )
        # TODO: implement handler

        logger.debug("finished")
        pass


from FinalProjectSimulator.simulation_runner.simulation_manager import SimulationManager
