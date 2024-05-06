from datetime import datetime
from models.passenger import Passenger
from models.stop import Stop
from line_manager import LineManager
from models.event import Event


class Bus:
    _id_counter = 1  # class-level variable to keep track of IDs

    def __init__(self, line_manager: LineManager):
        self.id = Bus._id_counter
        Bus._id_counter += 1
        self.line_manager = line_manager
        self.route: list[tuple[Stop, datetime]] = []
        self.last_stop: Stop = None
        self.next_stop: Stop = None
        self.passengers: list[Passenger] = []
        self.passengers_enroute: dict[tuple[Stop, Stop], int] = dict()

    def create_events(self) -> list[Event]:
        # TODO: 1. Create 'BusStart' event at time of departure
        # 2. If bus has a route defined (it is ordinary bus) create 'BusAtStop' event and 'BusFinish' after last stop
        pass

    def add_passenger(self, passenger: Passenger) -> bool:
        try:
            self.passengers.append(passenger)
            return True
        except Exception as e:
            print(e)
            return False

    def remove_passenger(self, passenger: Passenger) -> bool:
        try:
            self.passengers.remove(passenger)
            return True
        except Exception as e:
            print(e)
            return False

    def update_route(self, route: list[tuple[Stop, datetime]]) -> bool:
        try:
            self.route = route
            return True
        except Exception as e:
            print(e)
            return False

    def update_last_next_stop(self) -> bool:
        # TODO: Implement this method
        pass

    def update_passengers_enroute(self) -> int:
        # TODO: Implement this method
        pass
