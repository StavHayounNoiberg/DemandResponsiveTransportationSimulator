from datetime import datetime, timedelta
import heapq
from line_manager import LineManager
from models.event import Event
from models.passenger import Passenger
from models.simulation import Simulation
from random import choices
from route_manager import RouteManager


class SimulationManager:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
        self.queue: list[Event] = []
        self.passengers: list[Passenger] = []
        self.route_manager = RouteManager(simulation)
        self.line_manager = LineManager(simulation)

    def create_events(self) -> list[Event]:
        try:
            self.route_manager.create_stops()
            self.line_manager.create_buses()

            # call create_events for each bus and append events to the queue
            for bus in self.line_manager.buses:
                self.queue.append(bus.create_events())

            # TODO: create all passengers events

            heapq.heapify(self.queue)
            return self.queue
        except Exception as e:
            print(e)
            return []

    def peek_next_event(self) -> Event:
        if not self.queue:
            return None
        return self.queue[0]

    def pop_next_event(self) -> Event:
        if not self.queue:
            return None
        return heapq.heappop(self.queue)

    def insert_event(self, event: Event) -> bool:
        try:
            heapq.heappush(self.queue, event)
            return True
        except TypeError:
            print("Event must be an instance of the Event class")
            return False
        except Exception as e:
            print(e)
            return False

    def save_results(self) -> bool:
        # TODO: save_results should save all passengers and buses data to database

        self.simulation.set_duration()
        self.simulation.set_success(True)
        # TODO: save simulation to database
        pass

    # def create_events(
    #     self,
    #     event_times_distribution: DistributionTypes,
    #     reporting_rate: float,
    #     param,
    #     start_time: datetime,
    #     end_time: datetime,
    # ) -> list[Event]:
    #     if reporting_rate > 1:
    #         raise ValueError("future requests rate can not be greater than 1 (100%)")

    #     if event_times_distribution == DistributionTypes.POISSON:
    #         event_times = Distributions.create_event_times_poisson(
    #             param, start_time, end_time
    #         )
    #     elif event_times_distribution == DistributionTypes.RANDOM:
    #         event_times = Distributions.create_event_times_random(
    #             param, start_time, end_time
    #         )
    #     elif event_times_distribution == DistributionTypes.EMPIRIC:
    #         event_times = Distributions.create_event_times_empiric(
    #             param, start_time, end_time
    #         )

    #     requests_types_distribution = choices(
    #         [EventType.FUTURE_REQUEST, EventType.IMMEDIATE_REQUEST],
    #         [reporting_rate, 1 - reporting_rate],
    #         k=len(event_times),
    #     )

    #     for event_type, event_time in zip(requests_types_distribution, event_times):
    #         self.queue.append(
    #             Event(
    #                 event_time,
    #                 event_type,
    #                 # TODO: Add all parameters of Event
    #                 "line_id",
    #                 "stop_src",
    #                 "stop_dest",
    #                 event_time + timedelta(hours=1),
    #             )
    #         )

    #     # Calculate the total duration
    #     total_duration_hours = (
    #         end_time - start_time
    #     ).total_seconds() / 3600  # in hours

    #     for hour in range(int(total_duration_hours)):
    #         event_time = (start_time + timedelta(hours=hour)).replace(microsecond=0)
    #         self.queue.append(Event(event_time, EventType.FUTUTRE_REQUESTS_CALC))

    #     heapq.heapify(self.queue)
    #     return self.queue

    # def count_events_by_type(self):
    #     immediate_count = sum(
    #         1 for event in self.queue if event.get_type() == EventType.IMMEDIATE_REQUEST
    #     )
    #     future_count = sum(
    #         1 for event in self.queue if event.get_type() == EventType.FUTURE_REQUEST
    #     )
    #     calc_count = sum(
    #         1
    #         for event in self.queue
    #         if event.get_type() == EventType.FUTUTRE_REQUESTS_CALC
    #     )
    #     return immediate_count, future_count, calc_count

    # def get_queue_len(self) -> int:
    #     return len(self.queue)


# events_manager = EventsManager()
# events_manager.create_events(
#     DistributionTypes.POISSON,
#     0.2,
#     10,
#     datetime.now(),
#     datetime.now() + timedelta(hours=24),
# )

# immediate_count, future_count, calc_count = events_manager.count_events_by_type()
# request_events = immediate_count + future_count
# print("Total events:", events_manager.get_queue_len())
# print("Request events:", request_events)
# print("Immediate events:", immediate_count, "Ratio:", round(immediate_count / request_events, 2))
# print("Future events:", future_count, "Ratio:", round(future_count / request_events, 2))
# print("Calculation events:", calc_count)
# print("First event is:", events_manager.peek_next_event())
# first_event = events_manager.pop_next_event()
# print("Event taken out:", first_event)
# print("Next event is:", events_manager.peek_next_event())
