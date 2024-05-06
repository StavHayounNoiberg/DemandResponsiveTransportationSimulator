from event import Event
from models.bus import Bus
from models.stop import Stop
from simulation_manager import SimulationManager


class BusAtStop(Event):
    def __init__(self, simulation_manager: SimulationManager, bus: Bus, stop: Stop):
        super().__init__(simulation_manager)
        self.bus = bus
        self.stop = stop

    def handle(self) -> bool:
        # TODO: implement handler
        pass
