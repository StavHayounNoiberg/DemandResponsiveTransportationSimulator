from models.bus import Bus
from models.simulation import Simulation
from models.stop import Stop


class LineManager:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
        self.buses: list[Bus] = []

    def create_buses(self) -> list[Bus]:
        # TODO: 1. Creates all buses for the entire simulation time
        # 2. Defines for each bus if it’s an express bus or ordinary
        # 3. For each ordinary bus: calls "create_route"
        pass

    def find_next_express_bus(self, stop: Stop) -> Bus:
        # TODO: Implement this method
        pass
