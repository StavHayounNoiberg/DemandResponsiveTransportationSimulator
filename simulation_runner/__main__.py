from datetime import datetime
from .logging_config import setup_logging
from ..models.simulation import Simulation
from .simulation_manager import SimulationManager
import sys


# Set up logging
setup_logging(log_level=logging.DEBUG)
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
                logger.info("Simulation finished successfully")
                sys.exit(0)
            else:
                logger.info("Simulation finished with errors")
                logger.error("Error saving simulation results")
                sys.exit(1)
        else:
            logger.error("Missing parameters")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
