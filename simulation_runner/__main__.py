from datetime import datetime
import os
import sys
from FinalProjectSimulator.models.simulation import Simulation
from FinalProjectSimulator.simulation_runner.logging_config import setup_logging
from FinalProjectSimulator.simulation_runner.simulation_manager import SimulationManager


# Set up logging
root_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(root_dir, 'logs')
setup_logging(log_dir, log_level=10) # DEBUG level (10)
import logging

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # Get parameters sent from the command line (simulation_id, line_id, start_time, end_time, express_rate, reporting_rate, line_id)
    try:
        simulation_start_time = datetime.now()
        if len(sys.argv) >= 6:
            simulation_id = sys.argv[1]
            line_id = sys.argv[2]
            start_time = datetime.strptime(sys.argv[3], "%d-%m-%Y.%H:%M")
            end_time = datetime.strptime(sys.argv[4], "%d-%m-%Y.%H:%M")
            express_rate = float(sys.argv[5])
            reporting_rate = float(sys.argv[6])

            # Create an instance of Simulation and SimulationManager and create the events
            simulation = Simulation(
                simulation_id,
                line_id,
                start_time,
                end_time,
                express_rate,
                reporting_rate,
                simulation_start_time,
            )
            manager = SimulationManager(simulation)
            manager.create_events()

            logger.info("Simulation started")
            # Iterate over the events and handle them
            while manager.peek_next_event() is not None:
                event = manager.pop_next_event()
                event.handle()

            # Save the simulation results
            if manager.save_results() is True:
                logger.info("Simulation results saved successfully")
            else:
                logger.error("Simulation results were not saved successfully")
        else:
            logger.error("Missing parameters")
    except Exception as e:
        logger.error(e)
