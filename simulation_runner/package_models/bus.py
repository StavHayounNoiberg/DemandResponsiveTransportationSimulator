from datetime import datetime
import logging
from FinalProjectSimulator.simulation_runner.package_models.event import Event


logger = logging.getLogger(__name__)


class Bus:
    def __init__(self, id: int, line_manager, leave_time: datetime):
        self.id = id
        Bus._id_counter += 1
        self.line_manager = line_manager
        self.leave_time = leave_time
        self.route: list[tuple["Stop", datetime]] = []
        self.last_stop: Stop = None
        self.next_stop: Stop = None
        self.passengers: list["Passenger"] = []
        self.passengers_enroute: dict[tuple["Stop", "Stop"], int] = dict()

    def create_events(self) -> list[Event]:
        logger.debug("started")
        logger.info("Creating events for bus %d", self.id)
        events_list = [
            BusStart(self.line_manager.simulation_manager, self.leave_time, self)]
        events_list.append(BusAtStop(self.line_manager.simulation_manager,
                           stop[1], self, stop[0]) for stop in self.route)
        # TODO: decide if to use BusFinish event
        # events_list.append(BusFinish(self.line_manager.simulation_manager, self.route[-1][1], self))
        logger.debug("finished")
        return events_list

    def add_passenger(self, passenger: "Passenger") -> bool:
        logger.debug("started")
        logger.info("Adding passenger %d to bus %d", passenger.id, self.id)
        try:
            self.passengers.append(passenger)
            logger.debug("finished")
            return True
        except Exception as e:
            logger.error(e)
            return False

    def remove_passenger(self, passenger: "Passenger") -> bool:
        logger.debug("started")
        logger.info("Removing passenger %d from bus %d", passenger.id, self.id)
        try:
            self.passengers.remove(passenger)
            logger.debug("finished")
            return True
        except Exception as e:
            logger.error(e)
            return False

    def update_route(self, route: list[tuple["Stop", datetime]]) -> bool:
        logger.debug("started")
        logger.info("Updating route for bus %d", self.id)
        try:
            self.route = route
            logger.debug("finished")
            return True
        except Exception as e:
            logger.error(e)
            return False

    def update_last_next_stop(self) -> bool:
        logger.debug("started")
        logger.info("Updating last and next stop for bus %d", self.id)
        # TODO: Implement this method

        logger.debug("finished")
        pass

    def update_passengers_enroute(self) -> int:
        logger.debug("started")
        logger.info("Updating passengers enroute for bus %d", self.id)
        # TODO: Implement this method

        logger.debug("finished")
        pass


from FinalProjectSimulator.simulation_runner.package_models.bus_at_stop import BusAtStop
#from FinalProjectSimulator.simulation_runner.package_models.bus_finish import BusFinish
from FinalProjectSimulator.simulation_runner.package_models.bus_start import BusStart
from FinalProjectSimulator.simulation_runner.package_models.passenger import Passenger
from FinalProjectSimulator.simulation_runner.package_models.stop import Stop
