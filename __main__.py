import multiprocessing
import subprocess
import sys
import uuid


def main():
    # Get parameters sent from the command line (start_time, end_time, express_rate, reporting_rate, line_ids)
    if len(sys.argv) >= 7:
        start_time = sys.argv[1]
        end_time = sys.argv[2]
        express_rate = sys.argv[3]
        reporting_rate = sys.argv[4]
        iterations = sys.argv[5]
        ids_list = sys.argv[6:]
    else:
        start_time, end_time, express_rate, reporting_rate, iterations, ids_list = get_user_input()

    # Start all simulations
    processes_and_ids = []
    for line_id in ids_list:
        simulation_id = create_simulation_id()
        print(f"Starting simulation {simulation_id} for line {line_id}")
        simulation_command = [
            sys.executable,
            "-m",
            "FinalProjectSimulator.simulation_runner",
            simulation_id,
            line_id,
            start_time,
            end_time,
            express_rate,
            reporting_rate,
            iterations,
        ]
        process = multiprocessing.Process(
            target=subprocess.run, args=(simulation_command,))
        processes_and_ids.append((process, simulation_id))
        process.start()

    # Wait for all simulations to finish
    for pair in processes_and_ids:
        process = pair[0]
        process.join()

    # Start analyzer for all simulations
    simulation_ids = [id for _, id in processes_and_ids]
    analyzer_command = [
        sys.executable,
        "-m",
        "FinalProjectSimulator.simulation_analyzer",
    ]
    analyzer_command.extend(simulation_ids)
    
    process = multiprocessing.Process(
        target=subprocess.run, args=(analyzer_command,))
    process.start()
    process.join()


def get_user_input():
    # TODO: Delete this hard coded parameters
    return "23-06-2024.00:00", "30-06-2024.03:00", "0.2", "0.5", "4", ["10010-3-#"]
    start_datetime = input("Enter the start datetime (format: DD-MM-YYYY.HH:MM): ")
    end_datetime = input("Enter the end datetime (format: DD-MM-YYYY.HH:MM): ")
    express_rate = input("Enter the express rate: ")
    reporting_rate = input("Enter the reporting rate: ")
    iterations = input("Enter the number of iterations: ")
    ids_str = input("Enter the list of IDs separated by commas: ")
    ids_list = ids_str.split(",")
    return start_datetime, end_datetime, express_rate, reporting_rate, iterations, ids_list


def create_simulation_id():
    return str(uuid.uuid4())


if __name__ == "__main__":
    main()
