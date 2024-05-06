from datetime import datetime
from models.bus import Bus
from models.passenger import Passenger


class Stop:
    def __init__(self, stop_id: str):
        self.id = stop_id
        self.buses: list[tuple[Bus, datetime]] = []
        self.passengers: list[Passenger] = []

    def add_bus(self, bus: Bus) -> bool:
        try:
            self.buses.append(bus)
            return True
        except Exception as e:
            print(e)
            return False

    def remove_bus(self, bus: Bus) -> bool:
        try:
            self.buses.remove(bus)
            return True
        except Exception as e:
            print(e)
            return False

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
