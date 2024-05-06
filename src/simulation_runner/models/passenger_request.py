from datetime import datetime
from event import Event
from simulation_manager import SimulationManager


class PassengerRequest(Event):
    def __init__(
        self,
        simulation_manager: SimulationManager,
        line_id: str,
        stop_src: str,
        stop_dest: str,
        is_reporting: bool,
        leaving_time: datetime,
    ):
        super().__init__(simulation_manager)
        self.line_id = line_id
        self.stop_src = stop_src
        self.stop_dest = stop_dest
        self.is_reporting = is_reporting
        self.leaving_time = leaving_time

    def handle(self) -> bool:
        # TODO: implement handler
        pass
