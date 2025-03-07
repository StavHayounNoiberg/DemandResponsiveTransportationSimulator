from datetime import datetime
import logging
from FinalProjectSimulator.simulation_runner.package_models.event import Event


logger = logging.getLogger(__name__)


class BusAtStop(Event):
    def __init__(self, simulation_manager, time: datetime, bus: "Bus", stop: "Stop"):
        super().__init__(simulation_manager, time)
        self.bus = bus
        self.stop = stop

    def handle(self) -> bool:
        logger.debug("started")
        logger.info(
            "Event time: %s Event: BusAtStop for bus %d at stop %d",
            self.time.isoformat(),
            self.bus.id,
            self.stop.id,
        )
        if self.bus.update_last_next_stop() is False:
            logger.error("Failed to update last and next stops")
            logger.debug("finished")
            return False
        
        to_remove_from_bus = []
        for passenger in self.bus.passengers:
            if passenger.stop_dest == self.stop:
                passenger.update_arrival(self.time)
                to_remove_from_bus.append(passenger)
                
        for passenger in to_remove_from_bus:
            self.bus.remove_passenger(passenger)
                
        to_remove_from_stop = []
        for passenger in self.stop.passengers:
            if passenger.bus == self.bus:
                passenger.update_aboard(self.time)
                self.bus.add_passenger(passenger)
                to_remove_from_stop.append(passenger)
            
        for passenger in to_remove_from_stop:
            self.stop.remove_passenger(passenger)
        
        self.bus.update_passengers_enroute()
        
        self.stop.remove_bus(self.bus)

        logger.debug("finished")
        return True


from FinalProjectSimulator.simulation_runner.package_models.bus import Bus
from FinalProjectSimulator.simulation_runner.package_models.stop import Stop
