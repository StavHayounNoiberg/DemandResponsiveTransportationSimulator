from .event import Event


class BusFinish(Event):
    def __init__(self, simulation_manager: "SimulationManager", bus: "Bus"):
        super().__init__(simulation_manager)
        self.bus = bus

    def handle(self) -> bool:
        # TODO: implement handler
        pass


from .bus import Bus
from ..simulation_manager import SimulationManager
