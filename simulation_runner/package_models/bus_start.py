from datetime import datetime
import logging
from FinalProjectSimulator.simulation_runner.package_models.event import Event


logger = logging.getLogger(__name__)


class BusStart(Event):
    def __init__(self, simulation_manager, time: datetime, bus: "Bus"):
        super().__init__(simulation_manager, time)
        self.bus = bus

    def handle(self) -> bool:
        logger.debug("started")
        logger.info("Event time: %s Type: BusStart for bus %d", self.time.isoformat(), self.bus.id)
        
        if type(self.bus) is not Bus: # so it is express bus
            # remove the bus from all stops
            for stop, _ in self.bus.route:
                stop.remove_bus(self.bus)
            
            # create new route for the bus
            new_route = self.simulation_manager.route_manager.create_express_route(self.bus)
            if self.bus.update_route(new_route) is False:
                logger.error("Failed to update route for express bus %d", self.bus.id)
                logger.debug("finished")
                return False
            self.bus.clear_pending_stops()
            
            # add bus to all new stops
            for stop, stop_time in self.bus.route:
                stop.add_bus(self.bus, stop_time)
                
            # create events for bus stops
            for stop, stop_time in self.bus.route:
                if self.simulation_manager.insert_event(BusAtStop(self.simulation_manager, stop_time, self.bus, stop)) is False:
                    logger.error("Failed to insert BusAtStop event for stop %d", stop.id)
                    logger.debug("finished")
                    return False
                
            # TODO: decide if to use BusFinish event
            # if self.simulation_manager.insert_event(BusFinish(self.simulation_manager, self.bus.route[-1][1], self.bus)) is False:
            #     logger.error("Failed to insert BusFinish event")
            #     logger.debug("finished")
            #     return False
        
        self.bus.update_last_next_stop()            
            
        logger.debug("finished")
        return True


from FinalProjectSimulator.simulation_runner.package_models.bus import Bus
from FinalProjectSimulator.simulation_runner.package_models.bus_at_stop import BusAtStop
#from FinalProjectSimulator.simulation_runner.package_models.bus_finish import BusFinish
