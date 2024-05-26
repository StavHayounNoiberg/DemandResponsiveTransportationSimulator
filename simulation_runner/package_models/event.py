from datetime import datetime


class Event:
    _id_counter = 1  # class-level variable to keep track of IDs

    def __init__(self, simulation_manager, time: datetime = None):
        self.id = Event._id_counter
        Event._id_counter += 1
        self.time: datetime = time
        self.is_handled = False
        self.simulation_manager = simulation_manager

    def mark_handled(self):
        self.is_handled = True

    def __lt__(self, other) -> bool:
        if isinstance(other, Event):
            return self.get_time() < other.get_time()
        return NotImplemented

    def handle(self) -> bool:
        # abstract method, to be overridden by subclasses
        pass


# class EventType(Enum):
#     IMMEDIATE_REQUEST = 1
#     FUTURE_REQUEST = 2
#     FUTUTRE_REQUESTS_CALC = 3

# def __init__(
#     self,
#     time: datetime,
#     type: EventType,
#     line_id: str = None,
#     stop_src: str = None,
#     stop_dest: str = None,
#     requested_arrival: datetime = None,
# ):
#     self.id = Event._id_counter
#     Event._id_counter += 1
#     self.time = time
#     self.type = type
#     self.line_id = line_id
#     self.stop_src = stop_src
#     self.stop_dest = stop_dest
#     self.requested_arrival = requested_arrival
#     self.is_handled = False

# def get_event_id(self) -> int:
#     return self.id

# def get_time(self) -> datetime:
#     return self.time

# def get_type(self) -> EventType:
#     return self.type

# def get_line_id(self) -> str:
#     if self.get_type() != EventType.FUTUTRE_REQUESTS_CALC:
#         return self.line_id
#     else:
#         raise NotImplementedError("line_id is not supported for this event type")

# def get_stops(self) -> Tuple[str, str]:
#     if self.get_type() != EventType.FUTUTRE_REQUESTS_CALC:
#         return self.stop_src, self.stop_dest
#     else:
#         raise NotImplementedError("stops are not supported for this event type")

# def get_requested_arrival(self) -> datetime:
#     if self.get_type() != EventType.FUTUTRE_REQUESTS_CALC:
#         return self.requested_arrival
#     else:
#         raise NotImplementedError(
#             "requested arrival time is not supported for this event type"
#         )

# def get_handled_status(self) -> bool:
#     return self.is_handled

# def __str__(self):
#     status = "handled" if self.get_handled_status() else "not handled"

#     if self.get_type() != EventType.FUTUTRE_REQUESTS_CALC:
#         return f"Event with id: {self.get_event_id()}, of type: {self.get_type()}, at: {self.get_time()}, with status: {status}, for line: {self.get_line_id()}, with route: {self.get_stops()}, to arrive by: {self.get_requested_arrival()}"
#     else:
#         return f"Event with id: {self.get_event_id()}, of type: {self.get_type()}, at: {self.get_time()}, with status: {status}"
