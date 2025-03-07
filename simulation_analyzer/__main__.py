from datetime import timedelta
import logging
import os
import sys
import uuid
from FinalProjectSimulator.data_repo.simulation import PassengerData, BusData, get_analysis, get_buses, get_iteration_ids, get_passengers_by_simulation_id_and_assignment_reasons, get_passengers_by_simulation_id_and_assignment_reasons_to_exclude, get_simulation, save_analysis
from FinalProjectSimulator.models.simulation_analysis import SimulationAnalysis
from FinalProjectSimulator.simulation_runner.logging_config import setup_logging


# Set up logging
root_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(root_dir, 'logs')
setup_logging(log_dir, log_level=10)  # DEBUG level (10)

logger = logging.getLogger(__name__)


def calculate_avg_travel_time_for_passenger(iteration_id: str, passengers: list[PassengerData]):
    logger.info(f"Calculating average travel time for passengers in simulation {iteration_id}")
    passengers_data = passengers
    avg_travel_time_for_passenger = timedelta(seconds=0)
    for passenger in passengers_data:
        avg_travel_time_for_passenger += (passenger.arrival_time - passenger.aboard_time)

    if avg_travel_time_for_passenger > timedelta(seconds=0) and len(passengers_data) > 0:
        avg_travel_time_for_passenger = avg_travel_time_for_passenger.total_seconds() / 60
        avg_travel_time_for_passenger = avg_travel_time_for_passenger / (len(passengers_data))
    else:
        avg_travel_time_for_passenger = 0.0

    return avg_travel_time_for_passenger


def calculate_avg_waiting_time_for_passenger(iteration_id: str, passengers: list[PassengerData]):
    logger.info(f"Calculating average waiting time for passengers in simulation {iteration_id}")
    passengers_data = [p for p in passengers if p.assignment_reason == 0 or p.assignment_reason == 1]
    avg_waiting_time_for_passenger = timedelta(seconds=0)
    for passenger in passengers_data:
        avg_waiting_time_for_passenger += (passenger.aboard_time - passenger.leaving_time)

    if avg_waiting_time_for_passenger > timedelta(seconds=0) and len(passengers) > 0:
        avg_waiting_time_for_passenger = avg_waiting_time_for_passenger.total_seconds() / 60
        avg_waiting_time_for_passenger /= (len(passengers))
    else:
        avg_waiting_time_for_passenger = 0.0

    return avg_waiting_time_for_passenger


def calculate_avg_travel_time_for_bus(iteration_id: str, buses: list[BusData]):
    logger.info(f"Calculating average travel time for buses in simulation {iteration_id}")
    buses_data = buses
    avg_travel_time_for_bus = timedelta(seconds=0)
    for bus in buses_data:
        avg_travel_time_for_bus += (bus.final_dest_arrival_time - bus.leave_time)

    if avg_travel_time_for_bus > timedelta(seconds=0) and len(buses_data) > 0:
        avg_travel_time_for_bus = avg_travel_time_for_bus.total_seconds() / 60
        avg_travel_time_for_bus = avg_travel_time_for_bus / len(buses_data)
    else:
        avg_travel_time_for_bus = 0.0

    return avg_travel_time_for_bus


def calculate_rejected_passengers_rate(iteration_id: str):
    logger.info(f"Calculating rejected passengers rate in simulation {iteration_id}")
    rejected_passengers_data: list[PassengerData] = []
    all_passengers: list[PassengerData] = []
    rejected_passengers_data = get_passengers_by_simulation_id_and_assignment_reasons(iteration_id, [1, 6, 7])
    all_passengers = get_passengers_by_simulation_id_and_assignment_reasons_to_exclude(iteration_id, [8])

    return len(rejected_passengers_data) / len(all_passengers) if len(all_passengers) != 0 else 0


def calculate_dic_passengers_per_assignment(iteration_id: str, passengers: list[PassengerData]):
    logger.info(f"Calculating passengers per assignment in simulation {iteration_id}")
    passengers_dic = {}
    for i in range(8):
        passengers_data = [p for p in passengers if p.assignment_reason == i and p.arrival_time is not None and p.aboard_time is not None]
        passengers_dic[i] = len(passengers_data)

    return passengers_dic


def calculate_averages_across_iterations(analysis_data: "SimulationAnalysis", iterations_ids: list[str]):
    logger.info("Calculating averages across all iterations")

    # Create the passenger assingments dictionary
    for i in range(8):
        analysis_data.passengers_in_assignment[i] = 0.0

    # Calculate sum of each metric across all simulations
    for iteration_id in iterations_ids:
        passengers = get_passengers_by_simulation_id_and_assignment_reasons_to_exclude(iteration_id, [8])
        passengers = [p for p in passengers if p.arrival_time is not None and p.aboard_time is not None]
        analysis_data.avg_passengers_count += len(passengers)
        buses = get_buses(iteration_id)
        analysis_data.avg_bus_count += len(buses)
        analysis_data.avg_passenger_travel_time += calculate_avg_travel_time_for_passenger(iteration_id, passengers)
        analysis_data.avg_bus_travel_time += calculate_avg_travel_time_for_bus(iteration_id, buses)
        analysis_data.avg_passenger_waiting_time += calculate_avg_waiting_time_for_passenger(iteration_id, passengers)

        for assignment, value in calculate_dic_passengers_per_assignment(iteration_id, passengers).items():
            analysis_data.passengers_in_assignment[assignment] += value
            
    analysis_data.rejected_passengers = analysis_data.passengers_in_assignment[1] + analysis_data.passengers_in_assignment[6] + analysis_data.passengers_in_assignment[7]
    total_passengers = sum(analysis_data.passengers_in_assignment.values())
    analysis_data.rejected_passengers /= total_passengers if total_passengers > 0 else 0
    
    # Calculate averages (excluding the average passengers dictionary)
    logger.info("Calculating averages after all iterations data created")
    analysis_data.avg_passenger_travel_time /= len(iterations_ids)
    analysis_data.avg_bus_travel_time /= len(iterations_ids)
    analysis_data.avg_passenger_waiting_time /= len(iterations_ids)
    analysis_data.avg_passengers_count /= len(iterations_ids)
    analysis_data.avg_bus_count /= len(iterations_ids)

    for assignment in analysis_data.passengers_in_assignment.keys():
        analysis_data.passengers_in_assignment[assignment] /= len(iterations_ids)

    check_for_zero_state(analysis_data)


def check_for_zero_state(analysis_data: "SimulationAnalysis"):
    zero_state_analysis_data = get_analysis(analysis_data.line_id)
    if zero_state_analysis_data is None:
        if analysis_data.report_rate == 0.0 and analysis_data.express_rate == 0.0:
            logger.info("Transforming analysis data to zero state")
            analysis_data.id = analysis_data.line_id
        return


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

        express_rate += express_buses / all_buses if all_buses != 0 else 0

    return express_rate / len(iteration_ids)


if __name__ == "__main__":
    try:
        analysis_id = str(uuid.uuid4())
        logger.info("Starting analysis: %s", analysis_id)

        # get all the parameters from the command line arguments
        simulation_ids = sys.argv[1:]
        if len(simulation_ids) == 0:
            raise ValueError("No simulation ids were provided")

        iteration_ids = get_iteration_ids(simulation_ids)
        if len(iteration_ids) == 0:
            raise ValueError("No iteration ids were found")
        
        simulation_data = get_simulation(iteration_ids[0])
        report_rate = calculate_report_rate(iteration_ids)
        express_rate = calculate_express_rate(iteration_ids)
        analysis_data = SimulationAnalysis(analysis_id, simulation_ids, simulation_data.line_id, report_rate, express_rate)

        # for each simulation id, calculate all measures and create averages for each data type
        calculate_averages_across_iterations(analysis_data, iteration_ids)
        save_analysis(analysis_data)

    except Exception as e:
        logger.error(e)
