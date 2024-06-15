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
            return self.time < other.time
        return NotImplemented

    def handle(self) -> bool:
        # abstract method, to be overridden by subclasses
        pass
