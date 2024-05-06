from datetime import datetime
import multiprocessing
import subprocess
import sys
import uuid


def main():
    # Get parameters sent from the command line (start_time, end_time, express_rate, reporting_rate, line_ids)
    if len(sys.argv) >= 6:
        start_time = datetime.strptime(sys.argv[1], "%d-%m-%Y %H:%M")
        end_time = datetime.strptime(sys.argv[2], "%d-%m-%Y %H:%M")
        express_rate = float(sys.argv[3])
        reporting_rate = float(sys.argv[4])
        ids_list = sys.argv[5:]
    else:
        start_time, end_time, express_rate, reporting_rate, ids_list = get_user_input()

    # Start all simulations
    processes_and_ids = []
    for line_id in ids_list:
        simulation_id = create_simulation_id()
        simulation_command = [
            "python",
            "-m",
            "simulation_runner",
            simulation_id,
            line_id,
            start_time,
            end_time,
            express_rate,
            reporting_rate,
        ]
        process = multiprocessing.Process(
            target=subprocess.run, args=(simulation_command,)
        )
        processes_and_ids.append((process, simulation_id))
        process.start()

    # Wait for all simulations to finish
    for pair in processes_and_ids:
        process = pair[0]
        process.join()

    # Start all analyzers
    analyzer_processes = []
    for pair in processes_and_ids:
        id = pair[1]
        analyzer_command = [
            "python",
            "-m",
            "simulation_analyzer",
            id,
        ]
        process = multiprocessing.Process(
            target=subprocess.run, args=(analyzer_command,)
        )
        analyzer_processes.append(process)
        process.start()

    # Wait for all analyzers to finish
    for process in analyzer_processes:
        process.join()


def get_user_input():
    start_str = input("Enter the start datetime (format: YYYY-MM-DD HH:MM): ")
    start_datetime = datetime.strptime(start_str, "%d-%m-%Y %H:%M")

    end_str = input("Enter the end datetime (format: YYYY-MM-DD HH:MM): ")
    end_datetime = datetime.strptime(end_str, "%d-%m-%Y %H:%M")

    express_rate = float(input("Enter the express rate: "))
    reporting_rate = float(input("Enter the reporting rate: "))
    ids_str = input("Enter the list of IDs separated by commas: ")
    ids_list = ids_str.split(",")
    return start_datetime, end_datetime, express_rate, reporting_rate, ids_list


def create_simulation_id():
    return str(uuid.uuid4())


if __name__ == "__main__":
    main()
