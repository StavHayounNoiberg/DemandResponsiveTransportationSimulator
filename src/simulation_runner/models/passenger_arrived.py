from event import Event
from models.passenger import Passenger
from simulation_manager import SimulationManager


class PassengerArrived(Event):
    def __init__(self, simulation_manager: SimulationManager, passenger: Passenger):
        super().__init__(simulation_manager)
        self.passenger = passenger

    def handle(self) -> bool:
        # TODO: implement handler
        pass
