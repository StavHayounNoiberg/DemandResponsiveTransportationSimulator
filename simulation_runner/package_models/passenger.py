from datetime import datetime
import logging
from FinalProjectSimulator.simulation_runner.package_models.assignment_reason import AssignmentReason


logger = logging.getLogger(__name__)


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
        logger.debug("started")
        logger.info("Updating bus for passenger %d", self.id)
        try:
            self.bus = bus
            self.assignment_reason = assignment_reason
            logger.debug("finished")
            return True
        except Exception as e:
            logger.error(e)
            return False

    def update_aboard(self, time: datetime) -> bool:
        logger.debug("started")
        logger.info("Updating aboard time for passenger %d", self.id)
        try:
            self.aboard_time = time
            logger.debug("finished")
            return True
        except Exception as e:
            logger.error(e)
            return False

    def update_arrival(self, time: datetime) -> bool:
        logger.debug("started")
        logger.info("Updating arrival time for passenger %d", self.id)
        try:
            self.arrival_time = time
            logger.debug("finished")
            return True
        except Exception as e:
            logger.error(e)
            return False
