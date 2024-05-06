from datetime import datetime
from .assignment_reason import AssignmentReason


class Passenger:
    _id_counter = 1  # class-level variable to keep track of IDs

    def __init__(
        self,
        stop_src: str,
        stop_dest: str,
        reporting_time: datetime,
        leaving_time: datetime,
    ):
        self.id = Passenger._id_counter
        Passenger._id_counter += 1
        self.stop_src = stop_src
        self.stop_dest = stop_dest
        self.reporting_time = reporting_time
        self.leaving_time = leaving_time
        self.aboard_time: datetime = None
        self.arrival_time: datetime = None
        self.bus = None
        self.assignment_reason: AssignmentReason = None

    def update_bus(self, bus, assignment_reason) -> bool:
        try:
            self.bus = bus
            self.assignment_reason = assignment_reason
            return True
        except Exception as e:
            print(e)
            return False

    def update_aboard(self, time: datetime) -> bool:
        try:
            self.aboard_time = time
            return True
        except Exception as e:
            print(e)
            return False

    def update_arrival(self, time: datetime) -> bool:
        try:
            self.arrival_time = time
            return True
        except Exception as e:
            print(e)
            return False
