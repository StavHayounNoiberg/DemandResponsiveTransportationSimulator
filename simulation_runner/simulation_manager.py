from datetime import datetime, timedelta
import heapq
import logging
import numpy as np
from FinalProjectSimulator.data_repo.simulation import save_simulation, save_buses, save_passengers
from FinalProjectSimulator.data_repo.timeseries import get_timeseries_data_by_primary_key
from FinalProjectSimulator.data_repo.ridership import get_stations_passengers_by_day
from FinalProjectSimulator.models.simulation import Simulation
from FinalProjectSimulator.simulation_runner.line_manager import LineManager
from FinalProjectSimulator.simulation_runner.package_models.event import Event
from FinalProjectSimulator.simulation_runner.route_manager import RouteManager
from FinalProjectSimulator.utilities.datetime_utils import get_day_number, get_datetimes_between
from FinalProjectSimulator.utilities.distributions import create_datetimes_poisson_distribution


logger = logging.getLogger(__name__)


class SimulationManager:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
        self.queue: list[Event] = []
        self.passengers = []
        self.route_manager = RouteManager(simulation)
        self.line_manager = LineManager(self, simulation)

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

    def add_passenger(self, passenger) -> bool:
        self.passengers.append(passenger)
        return True

    def save_results(self) -> bool:
        logger.debug("started")
        logger.info("Saving simulation results")
        
        try:
            save_buses(self.simulation.id, self.line_manager.buses)
            save_passengers(self.simulation.id, self.passengers)
            self.simulation.set_success(True)
        except:
            self.simulation.set_success(False)
        
        try:
            self.simulation.set_duration()
            save_simulation(self.simulation)
        except:
            return False
        
        logger.debug("finished")
        return True

    def __create_passengers_events(self) -> list["PassengerRequest"]:
        logger.debug("started")
        logger.info("Creating passengers events")
        line_id = self.simulation.line_id
        start_time = self.simulation.start_time
        end_time = self.simulation.end_time

        date_list = get_datetimes_between(start_time, end_time)

        # Create the list of day numbers (1 for Sunday, 2 for Monday, ..., 7 for Saturday)
        day_numbers = [get_day_number(dt) for dt in date_list]

        # Create the list of datetimes for the passengers events
        datetimes: list[datetime] = []
        for i in range(len(date_list) - 1):
            start_date = date_list[i]
            end_date = date_list[i + 1]
            day_number = day_numbers[i]

            timeseries_data = get_timeseries_data_by_primary_key(
                self.simulation.line_id, day_number, "passengers")

            # Create poisson distribution of events for each hour in the day based on the timeseries data
            lambda_params = timeseries_data.iloc[0, 3:].tolist()
            datetimes.extend(create_datetimes_poisson_distribution(
                lambda_params, start_date, end_date))

        # Create the probabilities for each station based on the ridership data
        ridership_dfs = {day: get_stations_passengers_by_day(
            self.simulation.line_id, day) for day in set(day_numbers)}
        probabilities = {}
        for day, df in ridership_dfs.items():
            if len(df) > 1:
                df.loc[df.index[-2], df.columns[-1]] += df.iloc[-1, -1]
                df.loc[df.index[-1], df.columns[-1]] = 0

            daily_averages = df[df.columns[-1]]
            prob = daily_averages / daily_averages.sum()
            probabilities[day] = prob

        # Create the passenger events
        events: list[PassengerRequest] = []
        for leave_time in datetimes:
            day = get_day_number(leave_time)
            prob = probabilities[day]
            stops = self.route_manager.stops
            src_station = np.random.choice(stops, p=prob)
            optional_dsts = [
                stop for stop in self.route_manager.stops if stop.ordinal_number > src_station.ordinal_number]
            if not optional_dsts:
                logger.warning(
                    "No optional destinations for station %s, probably it is the last stop", src_station.name)
                continue
            dst_station = np.random.choice(optional_dsts)
            is_reporting = np.random.choice([True, False], p=[
                                            self.simulation.reporting_rate, 1 - self.simulation.reporting_rate])
            # TODO: implement reporting time logic
            report_time = (leave_time - timedelta(hours=1)
                           if is_reporting else leave_time)
            events.append(PassengerRequest(self, report_time, line_id,
                          src_station, dst_station, is_reporting, leave_time))

        logger.debug("finished")
        return events


from FinalProjectSimulator.simulation_runner.package_models.passenger_request import PassengerRequest
