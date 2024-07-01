import logging
from datetime import datetime
import os
import sys
import threading
from FinalProjectSimulator.models.simulation import Simulation
from FinalProjectSimulator.simulation_runner.logging_config import setup_logging
from FinalProjectSimulator.simulation_runner.simulation_manager import SimulationManager


BATCH_SIZE = os.cpu_count()


# Set up logging
root_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(root_dir, 'logs')
setup_logging(log_dir, log_level=20)  # DEBUG level (10)

logger = logging.getLogger(__name__)


def run_simulation(simulation_id, line_id, start_time, end_time, express_rate, reporting_rate):
    # Create an instance of Simulation and SimulationManager and create the events
    simulation_start_time = datetime.now()
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

    logger.info("Simulation %s started", simulation_id)
    # Iterate over the events and handle them
    while manager.peek_next_event() is not None:
        event = manager.pop_next_event()
        event.handle()
        event.mark_handled()

    # Save the simulation results
    if manager.save_results() is True:
        logger.info("Simulation results saved successfully")
    else:
        logger.error("Simulation results were not saved successfully")


if __name__ == "__main__":
    # Get parameters sent from the command line (simulation_id, line_id, start_time, end_time, express_rate, reporting_rate, line_id)
    try:
        logger.info("Simulation starting")
        if len(sys.argv) == 8:
            simulation_id = sys.argv[1]
            line_id = sys.argv[2]
            start_time = datetime.strptime(sys.argv[3], "%d-%m-%Y.%H:%M")
            end_time = datetime.strptime(sys.argv[4], "%d-%m-%Y.%H:%M")
            express_rate = float(sys.argv[5])
            reporting_rate = float(sys.argv[6])
            iterations = int(sys.argv[7])
            
            threads = []
            for i in range(iterations):
                iteration_id = f"{simulation_id}/{i}"
                thread_name = f"Iteration {i}"
                thread = threading.Thread(target=run_simulation, name=thread_name, args=(iteration_id, line_id, start_time, end_time, express_rate, reporting_rate))
                threads.append(thread)
                
                if len(threads) == BATCH_SIZE or i == iterations - 1:
                    for thread in threads:
                        thread.start()
            
                    for thread in threads:
                        thread.join()

                    threads = []
                
        else:
            logger.error("Missing parameters")
    except Exception as e:
        logger.error(e)
