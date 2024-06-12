import logging
import os
import sys
import uuid
from FinalProjectSimulator.data_repo.simulation import save_analysis
from FinalProjectSimulator.simulation_runner.logging_config import setup_logging


# Set up logging
root_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(root_dir, 'logs')
setup_logging(log_dir, log_level=10)  # DEBUG level (10)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        logger.info("Analyzer starting")
        analysis_id = str(uuid.uuid4())
        # get all the parameters from the command line arguments
        simulation_ids = sys.argv
        
        # for each simulation id, calculate all measures
        
        
        
        #save_analysis(a, b, c, d)


    except Exception as e:
        logger.error(e)
