from datetime import datetime
import logging


logger = logging.getLogger(__name__)


class Stop:
    def __init__(self, stop_id: str, ordinal_number: int, name: str, location: tuple[float, float]):
        self.id = stop_id
        self.ordinal_number = ordinal_number
        self.name = name
        self.location = location
        self.buses: list[tuple["Bus", datetime]] = []
        self.passengers: list["Passenger"] = []

    def add_bus(self, bus: "Bus") -> bool:
        logger.debug("started")
        logger.info("Adding bus %d to stop %d", bus.id, self.id)
        try:
            self.buses.append(bus)
            logger.debug("finished")
            return True
        except Exception as e:
            logger.error(e)
            return False

    def remove_bus(self, bus: "Bus") -> bool:
        logger.debug("started")
        logger.info("Removing bus %d from stop %d", bus.id, self.id)
        try:
            self.buses.remove(bus)
            logger.debug("finished")
            return True
        except Exception as e:
            logger.error(e)
            return False

    def add_passenger(self, passenger: "Passenger") -> bool:
        logger.debug("started")
        logger.info("Adding passenger %d to stop %d", passenger.id, self.id)
        try:
            self.passengers.append(passenger)
            logger.debug("finished")
            return True
        except Exception as e:
            logger.error(e)
            return False

    def remove_passenger(self, passenger: "Passenger") -> bool:
        logger.debug("started")
        logger.info("Removing passenger %d from stop %d", passenger.id, self.id)
        try:
            self.passengers.remove(passenger)
            logger.debug("finished")
            return True
        except Exception as e:
            logger.error(e)
            return False


from FinalProjectSimulator.simulation_runner.package_models.bus import Bus
from FinalProjectSimulator.simulation_runner.package_models.passenger import Passenger
