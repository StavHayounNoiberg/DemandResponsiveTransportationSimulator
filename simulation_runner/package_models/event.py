from datetime import datetime


class Event:
    __id_counter = 1  # class-level variable to keep track of IDs

    def __init__(self, simulation_manager, time: datetime = None):
        self.id = Event.__id_counter
        Event.__id_counter += 1
        self.time: datetime = time
        self.is_handled = False
        self.simulation_manager = simulation_manager

    def mark_handled(self):
        self.is_handled = True

    def __lt__(self, other) -> bool:
        if isinstance(other, Event):
            if self.time != other.time:
                return self.time < other.time
            else:
                priority = {"PassengerArrived": 5, "PassengerRequest": 4, "BusStart": 3, "BusAtStop": 2, "BusFinish": 1}
                return priority.get(self.__class__.__name__, 0) > priority.get(other.__class__.__name__, 0)
        return NotImplemented
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Event):
            return False
        return self.id == value.id
    
    def __hash__(self) -> int:
        return hash(self.id)

    def handle(self) -> bool:
        # abstract method, to be overridden by subclasses
        pass
