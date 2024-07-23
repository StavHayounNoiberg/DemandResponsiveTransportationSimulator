from datetime import datetime
import logging
from FinalProjectSimulator.simulation_runner.package_models.bus import Bus


logger = logging.getLogger(__name__)


class ExpressBus(Bus):
    def __init__(self, id: int, line_manager, leave_time: datetime):
        super().__init__(id, line_manager, leave_time)
        self.pending_stops: list["Stop"] = []
    
    def add_stop(self, stop: "Stop") -> bool:
        logger.debug("started")
        logger.info("Adding stop %d to express bus %d", stop.id, self.id)
        try:
            if stop not in self.pending_stops:
                self.pending_stops.append(stop)
            logger.debug("finished")
            return True
        except Exception as e:
            logger.error(e)
            raise e
        
    def set_pending_stops(self, stops: list["Stop"]) -> bool:
        logger.debug("started")
        logger.info("Setting pending stops for express bus %d", self.id)
        try:
            self.pending_stops = stops
            logger.debug("finished")
            return True
        except Exception as e:
            logger.error(e)
            raise e

    def clear_pending_stops(self) -> bool:
        logger.debug("started")
        logger.info("Clearing pending stops for express bus %d", self.id)
        try:
            self.pending_stops.clear()
            logger.debug("finished")
            return True
        except Exception as e:
            logger.error(e)
            raise e


from FinalProjectSimulator.simulation_runner.package_models.stop import Stop
