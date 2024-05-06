from datetime import datetime
from ..models.simulation import Simulation
from .package_models.bus import Bus
from .package_models.stop import Stop


class RouteManager:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
        self.stops: list[Stop] = []

    def create_stops(self) -> list[Stop]:
        # TODO: Create all the stops for the line
        pass

    def create_route(self, bus: Bus) -> list[tuple[Stop, datetime]]:
        # TODO: 1. Updates the route of the bus with the list of stops and arrival times by using "update_route"
        # 2. Updates each stop's buses list with the bus and the arrival time by using "add_bus"

        pass

    def create_express_route(self, bus: Bus) -> list[tuple[Stop, datetime]]:
        # TODO: Think how to do this. At the end should updates each stop's buses list with the bus and the arrival time by using "add_bus"
        pass
