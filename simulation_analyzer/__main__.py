from datetime import timedelta
import logging
import os
import sys
import uuid
from FinalProjectSimulator.data_repo.simulation import PassengerData, BusData, get_buses, get_passengers_by_simulation_id_and_assignment_reasons, get_passengers_by_simulation_id_and_assignment_reasons_to_exclude, get_simulation, save_analysis 
from FinalProjectSimulator.models.simulation_analysis import SimulationAnalysis
from FinalProjectSimulator.simulation_runner.logging_config import setup_logging


# Set up logging
root_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(root_dir, 'logs')
setup_logging(log_dir, log_level=10)  # DEBUG level (10)

logger = logging.getLogger(__name__)


def calculate_avg_travel_time_for_passenger(iteration_id: str):
    logger.info(f"Calculating average travel time for passengers in simulation {iteration_id}")
    passengers_data: list[PassengerData] = []
    passengers_data = get_passengers_by_simulation_id_and_assignment_reasons_to_exclude(iteration_id, [8])
    avg_travel_time_for_passenger = timedelta(seconds=0)
    for passenger in passengers_data:
        avg_travel_time_for_passenger += (passenger.arrival_time - passenger.aboard_time)

    if avg_travel_time_for_passenger != timedelta(seconds=0):
        avg_travel_time_for_passenger = avg_travel_time_for_passenger.total_seconds() / 60
        avg_travel_time_for_passenger = avg_travel_time_for_passenger / (len(passengers_data))

    return avg_travel_time_for_passenger


def calculate_avg_waiting_time_for_passenger(iteration_id: str):
    logger.info(f"Calculating average waiting time for passengers in simulation {iteration_id}")
    order_in_advance_passengers_data: list[PassengerData] = []
    other_passengers_data: list[PassengerData] = []
    # passengers who ordered in advance have waiting time = 0 
    order_in_advance_passengers_data = get_passengers_by_simulation_id_and_assignment_reasons(iteration_id, [2, 3])
    other_passengers_data = get_passengers_by_simulation_id_and_assignment_reasons_to_exclude(iteration_id, [2, 3, 8])
    avg_waiting_time_for_passenger = timedelta(seconds=0)
    for passenger in other_passengers_data:
        avg_waiting_time_for_passenger += (passenger.aboard_time - passenger.leaving_time)
       
    if avg_waiting_time_for_passenger != timedelta(seconds=0):
        avg_waiting_time_for_passenger = avg_waiting_time_for_passenger.total_seconds() / 60
        avg_waiting_time_for_passenger = avg_waiting_time_for_passenger / (len(other_passengers_data) + len(order_in_advance_passengers_data)) 
    
    return avg_waiting_time_for_passenger


def calculate_avg_travel_time_for_bus(iteration_id: str):
    logger.info(f"Calculating average travel time for buses in simulation {iteration_id}")
    buses_data: list[BusData] = []
    buses_data = get_buses(iteration_id)
    avg_travel_time_for_bus = timedelta(seconds=0)
    for bus in buses_data:
        avg_travel_time_for_bus += (bus.final_dest_arrival_time - bus.leave_time)

    if avg_travel_time_for_bus != timedelta(seconds=0):
        avg_travel_time_for_bus = avg_travel_time_for_bus.total_seconds() / 60
        avg_travel_time_for_bus = avg_travel_time_for_bus / len(buses_data)
    
    return avg_travel_time_for_bus


def calculate_rejected_passengers_rate(iteration_id: str):
    logger.info(f"Calculating rejected passengers rate in simulation {iteration_id}")
    rejected_passengers_data: list[PassengerData] = []
    all_passengers: list[PassengerData] = []
    rejected_passengers_data = get_passengers_by_simulation_id_and_assignment_reasons(iteration_id, [1, 6, 7])
    all_passengers = get_passengers_by_simulation_id_and_assignment_reasons_to_exclude(iteration_id, [8])

    return len(rejected_passengers_data) / len(all_passengers) if len(all_passengers) != 0 else 0


def calculate_dic_passengers_per_assignment(iteration_id : str):
    logger.info(f"Calculating passengers per assignment in simulation {iteration_id}")
    passengers_dic = {}
    passengers_data: list[PassengerData] = []
    for i in range(8):
        passengers_data = get_passengers_by_simulation_id_and_assignment_reasons(iteration_id, [i])
        passengers_dic[i] = len(passengers_data)
    
    return passengers_dic


def calculate_averages_across_iterations(analysis_data: "SimulationAnalysis", iterations_ids: list[str]):
    logger.info("Calculating averages across all iterations")
    
    # Create the passenger assingments dictionary
    for i in range(8):
        analysis_data.passengers_in_assignment[i] = 0.0

    # Calculate sum of each metric across all simulations
    for iteration_id in iterations_ids:
        analysis_data.avg_travel_time_for_passenger += calculate_avg_travel_time_for_passenger(iteration_id)
        analysis_data.avg_travel_time_for_bus += calculate_avg_travel_time_for_bus(iteration_id)
        analysis_data.avg_waiting_time_for_passenger += calculate_avg_waiting_time_for_passenger(iteration_id)
        analysis_data.rejected_passengers += calculate_rejected_passengers_rate(iteration_id)
        
        for assignment, value in calculate_dic_passengers_per_assignment(iteration_id).items():
            analysis_data.passengers_in_assignment[assignment] += value

    # Calculate averages (excluding the average passengers dictionary)
    logger.info("Calculating averages after all iterations data created")
    analysis_data.avg_travel_time_for_passenger = analysis_data.avg_travel_time_for_passenger / len(iterations_ids)
    analysis_data.avg_travel_time_for_bus = analysis_data.avg_travel_time_for_bus / len(iterations_ids)
    analysis_data.avg_waiting_time_for_passenger = analysis_data.avg_waiting_time_for_passenger / len(iterations_ids)
    analysis_data.rejected_passengers = analysis_data.rejected_passengers / len(iterations_ids)
    
    for assignment in analysis_data.passengers_in_assignment.keys():
            analysis_data.passengers_in_assignment[assignment] /= len(iterations_ids)
            
    normalize_metrics(analysis_data)
    
    
def normalize_metrics(analysis_data: "SimulationAnalysis"):
    logger.info("Normalizing metrics with zero state")
    zero_state_analysis_data = get_simulation(analysis_data.line_id)
    if zero_state_analysis_data is None:
        if analysis_data.report_rate == 0.0 and analysis_data.express_rate == 0.0:
            analysis_data.id = analysis_data.line_id
        return
    
    analysis_data.avg_travel_time_for_passenger = analysis_data.avg_travel_time_for_passenger / zero_state_analysis_data.avg_travel_time_for_passenger
    analysis_data.avg_travel_time_for_bus = analysis_data.avg_travel_time_for_bus / zero_state_analysis_data.avg_travel_time_for_bus
    analysis_data.avg_waiting_time_for_passenger = analysis_data.avg_waiting_time_for_passenger / zero_state_analysis_data.avg_waiting_time_for_passenger

    
def calculate_report_rate(iteration_ids: list[str]):
    logger.info("Calculating general report rate")
    report_rate = 0.0
    for iteration_id in iteration_ids:
        report_passengers = 0
        all_passengers = 0
        passengers_data = get_passengers_by_simulation_id_and_assignment_reasons_to_exclude(iteration_id, [8])
        for passenger in passengers_data:
            all_passengers += 1
            if passenger.reporting_time != passenger.leaving_time:
                report_passengers += 1
                
        report_rate += report_passengers / all_passengers if all_passengers != 0 else 0

    return report_rate / len(iteration_ids)    
    

def calculate_express_rate(iteration_ids: list[str]):
    logger.info("Calculating general express rate")
    express_rate = 0.0
    for iteration_id in iteration_ids:
        express_buses = 0
        all_buses = 0
        buses_data = get_buses(iteration_id)
        for bus in buses_data:
            all_buses += 1
            if bus.is_express:
                express_buses += 1
                
        express_rate += express_buses / all_buses

    return express_rate / len(iteration_ids)


if __name__ == "__main__":
    try:
        logger.info("Analyzer starting")
        analysis_id = str(uuid.uuid4())
        
        # get all the parameters from the command line arguments
        iteration_ids = sys.argv[1:]
        if len(iteration_ids) == 0:
            raise ValueError("No simulation ids were provided")
        
        simulation_data = get_simulation(iteration_ids[0])
        report_rate = calculate_report_rate(iteration_ids)
        express_rate = calculate_express_rate(iteration_ids)
        analysis_data = SimulationAnalysis(analysis_id, simulation_data.line_id, report_rate, express_rate)
        
        # for each simulation id, calculate all measures and create averages for each data type
        calculate_averages_across_iterations(analysis_data, iteration_ids)
        save_analysis(analysis_data)

    except Exception as e:
        logger.error(e)
