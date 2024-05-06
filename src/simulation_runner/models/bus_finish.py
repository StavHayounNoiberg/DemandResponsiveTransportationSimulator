from event import Event
from models.bus import Bus
from simulation_manager import SimulationManager


class BusFinish(Event):
    def __init__(self, simulation_manager: SimulationManager, bus: Bus):
        super().__init__(simulation_manager)
        self.bus = bus

    def handle(self) -> bool:
        # TODO: implement handler
        pass
