from FinalProjectSimulator.simulation_runner.simulation_manager import SimulationManager
from FinalProjectSimulator.simulation_runner.package_models.express_bus import ExpressBus, Bus, Stop
from datetime import datetime, timedelta
import logging
from FinalProjectSimulator.simulation_runner.package_models.event import Event
from FinalProjectSimulator.simulation_runner.package_models.passenger import Passenger, AssignmentReason
from FinalProjectSimulator.simulation_runner.package_models.passenger_arrived import PassengerArrived


logger = logging.getLogger(__name__)


class PassengerRequest(Event):
    def __init__(
        self,
        simulation_manager: "SimulationManager",
        time: datetime,
        line_id: str,
        stop_src: "Stop",
        stop_dest: "Stop",
        is_reporting: bool,
        leaving_time: datetime,
    ):
        super().__init__(simulation_manager, time)
        self.line_id = line_id
        self.stop_src: "Stop" = stop_src
        self.stop_dest: "Stop" = stop_dest
        self.is_reporting: bool = is_reporting
        self.leaving_time: datetime = leaving_time

    def handle(self) -> bool:
        logger.debug("started")
        logger.info("Event time: %s Type: PassengerRequest with id %d", self.time.isoformat(), self.id)
        passenger = Passenger(self.stop_src, self.stop_dest,
                              self.time, self.leaving_time)
        self.simulation_manager.add_passenger(passenger)
        
        # find the bus in the source stop buses list that arrives first to the destination stop
        source_buses = []
        end_of_day = self.leaving_time.replace(hour=0, minute=0, second=0) + timedelta(days=1)

        for bus, stop_time in self.stop_src.buses:
            if stop_time >= self.leaving_time and stop_time < end_of_day:
                source_buses.append(bus)
                
        next_express_bus = self.simulation_manager.line_manager.find_next_express_bus(
                passenger.stop_src, passenger.leaving_time)
        earliest_bus = self.simulation_manager.route_manager.earliest_bus_arriving_stop(
            source_buses, self.stop_dest)
        if earliest_bus is None:
            logger.error("No bus found for passenger %d", passenger.id)
            passenger.update_bus(None, AssignmentReason.NO_BUS)
            return False
        
        if self.is_reporting:
            logger.debug(
                "Creating PassengerArrived event for passenger %d", passenger.id)
            event = PassengerArrived(
                self.simulation_manager, self.leaving_time, passenger)
            if self.simulation_manager.insert_event(event) is False:
                logger.error(
                    "PassengerArrived event for passenger %d was not inserted", passenger.id)
                return False
            
            # assign the passenger to the earliest bus and specify the reason
            if next_express_bus is not None:  # if there is an express bus in future
                if next_express_bus.leave_time > passenger.reporting_time:  # if reported on time
                    if type(earliest_bus) is ExpressBus:  # if the earliest bus is an express bus
                        if earliest_bus == next_express_bus:  # if the earliest bus is the next express bus
                            next_express_bus.add_stop(passenger.stop_src)
                            next_express_bus.add_stop(passenger.stop_dest)
                            passenger.update_bus(next_express_bus, AssignmentReason.EXPRESS)
                        else:  # should not happen (logically)
                            logger.error("Missing case! passenger reported before next express bus arrives to the source stop," +
                                            " earliest bus is of type express, but the earliest bus is not the next express bus")
                            passenger.update_bus(None, AssignmentReason.NO_BUS)
                            return False
                    else:  # if the earliest bus is an ordinary bus
                        passenger.update_bus(earliest_bus, AssignmentReason.ORDINARY_IS_FASTER)
                else:  # if reported late
                    if type(earliest_bus) is ExpressBus:  # if the earliest bus is an express bus
                        if earliest_bus == next_express_bus:  # if the earliest bus is the next express bus
                            passenger.update_bus(next_express_bus, AssignmentReason.LUCKY_EXPRESS_REPORTING)
                        else:  # if the earliest bus is not the next express bus, but its still an express bus
                            passenger.update_bus(earliest_bus, AssignmentReason.LATE_REPORT_EXPRESS)
                    else:  # if the earliest bus is an ordinary bus
                        # if the next express bus stops at the source and destination stops (but still not the fastest)
                        if all(any(stop == s for stop, _ in next_express_bus.route) for s in [self.stop_src, self.stop_dest]):
                            passenger.update_bus(earliest_bus, AssignmentReason.LUCKY_ORDINARY_IS_FASTER)
                        else:  # if the next express bus does not stop at the source and destination stops
                            passenger.update_bus(earliest_bus, AssignmentReason.LATE_REPORT)
            else:  # if there is no express bus in future
                if type(earliest_bus) is ExpressBus:
                    logger.error("Missing case! no next_express_bus but the earliest_bus is of type ExpressBus")
                    passenger.update_bus(None, AssignmentReason.NO_BUS)
                    return False
                passenger.update_bus(earliest_bus, AssignmentReason.ORDINARY_IS_FASTER)
                
        else: # if not reporting
            passenger_bus = next((bus for bus, bus_time in passenger.stop_src.buses 
                                  if type(bus) is Bus 
                                  and bus_time >= passenger.leaving_time),
                                 None)
            if passenger_bus is None:
                logger.error("No ordinary bus found for passenger %d", passenger.id)
                passenger.update_bus(None, AssignmentReason.NO_BUS)
                return False
            
            if not passenger.stop_src.add_passenger(passenger):
                logger.error("Passenger %d was not added to source stop", passenger.id)
                return False
            
            if type(earliest_bus) is ExpressBus:
                passenger.update_bus(passenger_bus, AssignmentReason.ORDINARY_REJECTED)
            else:
                passenger.update_bus(passenger_bus, AssignmentReason.ORDINARY)
                
        logger.debug("finished")
        return True
