from datetime import datetime, timedelta
import heapq
import logging
import numpy as np
from FinalProjectSimulator.data_repo.timeseries import fetch_timeseries_data_by_primary_key
from FinalProjectSimulator.data_repo.ridership import fetch_stations_passengers_by_day
from FinalProjectSimulator.models.simulation import Simulation
from FinalProjectSimulator.simulation_runner.line_manager import LineManager
from FinalProjectSimulator.simulation_runner.package_models.event import Event
from FinalProjectSimulator.simulation_runner.route_manager import RouteManager
from FinalProjectSimulator.utilities.distributions import create_datetimes_poisson_distribution


logger = logging.getLogger(__name__)


class SimulationManager:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
        self.queue: list[Event] = []
        self.passengers = []
        self.route_manager = RouteManager(simulation)
        self.line_manager = LineManager(simulation)

    def create_events(self) -> list[Event]:
        logger.debug("started")
        logger.info("Creating simulation events")
        try:
            self.route_manager.create_stops()
            self.line_manager.create_buses()

            # call create_events for each bus and append events to the queue
            for bus in self.line_manager.buses:
                self.queue.extend(bus.create_events())

            # call create_passengers_events and append events to the queue
            self.queue.extend(self.__create_passengers_events())

            # turn the queue into a heap
            heapq.heapify(self.queue)
            logger.debug("finished")
            return self.queue
        except Exception as e:
            logger.error(e)
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
            logger.error("Event must be an instance of the Event class")
            return False
        except Exception as e:
            logger.error(e)
            return False

    def save_results(self) -> bool:
        logger.debug("started")
        logger.info("Saving simulation results")
        # TODO: save_results should save all passengers and buses data to database

        self.simulation.set_duration()
        self.simulation.set_success(True)
        # TODO: save simulation to database

        logger.debug("finished")
        return True
    
    def __create_passengers_events(self) -> list["PassengerRequest"]:
        logger.debug("started")
        logger.info("Creating passengers events")
        line_id = self.simulation.line_id
        start_time = self.simulation.start_time
        end_time = self.simulation.end_time

        # Initialize the list with the start_time
        date_list = [start_time]

        # Calculate the next midnight after the start_time
        current_date = start_time.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)

        # Add midnights until the day before the end_time
        while current_date < end_time:
            date_list.append(current_date)
            current_date += timedelta(days=1)

        # Add the end_time
        date_list.append(end_time)

        # Create the list of day numbers (1 for Sunday, 2 for Monday, ..., 7 for Saturday)
        day_numbers = [(dt.weekday() + 1) % 7 + 1 for dt in date_list]

        # Create the list of datetimes for the passengers events
        datetimes: list[datetime] = []
        for i in range(len(date_list) - 1):
            start_date = date_list[i]
            end_date = date_list[i + 1]
            day_number = day_numbers[i]

            timeseries_data = fetch_timeseries_data_by_primary_key(
                self.simulation, day_number, "passengers"
            )

            # Create poisson distribution of events for each hour in the day based on the timeseries data
            lambda_params = timeseries_data.iloc[0, 3:].tolist()
            datetimes.extend(
                create_datetimes_poisson_distribution(
                    lambda_params, start_date, end_date
                )
            )

        # Create the probabilities for each station based on the ridership data
        ridership_dfs = {
            day: fetch_stations_passengers_by_day(self.simulation.line_id, day)
            for day in set(day_numbers)
        }

        probabilities = {}
        for day, df in ridership_dfs.items():
            daily_averages = df[df.columns[-1]]
            prob = daily_averages / daily_averages.sum()
            probabilities[day] = prob

        # Create the passenger events
        events: list[PassengerRequest] = []
        for leave_time in datetimes:
            day = (leave_time.weekday() + 1) % 7 + 1
            prob = probabilities[day]
            stops = self.route_manager.stops
            src_station = np.random.choice(stops, p=prob)
            optional_dsts = [
                stop
                for stop in self.route_manager.stops
                if stop.ordinal_number > src_station.ordinal_number
            ]
            if not optional_dsts:
                logger.warning("No optional destinations for station %s, probably it is the last stop", src_station.name)
                continue
            dst_station = np.random.choice(optional_dsts)
            is_reporting = np.random.choice(
                [True, False],
                p=[self.simulation.reporting_rate, 1 - self.simulation.reporting_rate],
            )
            # TODO: implement reporting time logic
            report_time = (
                leave_time - timedelta(hours=1) if is_reporting else leave_time
            )
            events.append(
                PassengerRequest(
                    self,
                    report_time,
                    line_id,
                    src_station,
                    dst_station,
                    is_reporting,
                    leave_time,
                )
            )

        logger.debug("finished")
        return events
    
    
from FinalProjectSimulator.simulation_runner.package_models.passenger_request import PassengerRequest

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
