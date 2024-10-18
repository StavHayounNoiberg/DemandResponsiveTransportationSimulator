# Demand Responsive Transportation Simulator
Final Project of Industrial Engineering & Computer Science B.Sc at Afeka Academic College of Engineering

## Overview
The Demand Responsive Transportation Simulator is a key component of the project, developed to support decision-making and policy evaluation. The simulator is designed to model a transportation system where bus routes dynamically adapt based on real-time passenger demand. Specifically, the system explores a mixed operational mode where some buses run as "Express" buses, skipping unnecessary stops, while others continue operating on regular schedules.

The simulation generates detailed data on several key factors, including average travel time, wait time, and passenger service rates for each bus line. These metrics enable a comprehensive comparison of different operational policies, helping decision-makers evaluate the most efficient balance between regular and express bus services. By analyzing multiple policies over a short period, the simulator provides insights into the system's potential performance before implementing changes in the field​.

## Getting Started

### Prerequisites
- Python 3.x
- Required Python packages (listed in `requirements.txt`)

### Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/StavHayounNoiberg/DemandResponsiveTransportationSimulator.git
    ```
2. Navigate to the project directory:
    ```sh
    cd DemandResponsiveTransportationSimulator
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## MySQL Database Configuration

Before running the simulator, you need to insert your MySQL database information into the [`db_config.ini`](#file:db_config.ini-context) file. This configuration file is essential for connecting to the MySQL database used by the project.

### Steps to Insert Database Information

1. Open the [`db_config.ini`](#file:db_config.ini-context) file.
2. Locate the `[mysql]` section.
3. Replace the placeholder values with your actual MySQL database information.

### Example

```ini
[mysql]
host = your_database_host
user = your_database_user
password = your_database_password
charset = utf8
max_allowed_packet = 16M
```

### Database Setup

The database should be created by the [PublicTransportationDataAnalysis](https://github.com/StavHayounNoiberg/PublicTransportationDataAnalysis) project. Follow the instructions in that project to set up the database schema and initial data.

Alternatively, you can contact me to get DB backup files that can be loaded into your MySQL instance.

## Google Routes API Keys

Before running the simulator, you need to insert your Google Routes API keys into the `gmaps.py` file. The API keys are required to access the Google Maps services for route calculations.

### Steps to Insert API Keys

1. Open the `gmaps.py` file.
2. Locate the `API_KEYS` list.
3. Replace the placeholder API keys with your own valid Google Routes API keys.

### Example

```python
API_KEYS = [
    "YOUR_API_KEY_1",
    "YOUR_API_KEY_2",
    "YOUR_API_KEY_3",
    ...
]
```

## Running the Project
To run the simulation provide the following command line arguments:
The script can be run with command line arguments. The required arguments are:

1. `start_time`: The start datetime in the format `DD-MM-YYYY.HH:MM`.
2. `end_time`: The end datetime in the format `DD-MM-YYYY.HH:MM`.
3. `express_rate`: The express rate.
4. `reporting_rate`: The reporting rate.
5. `iterations`: The number of iterations.
6. `line_ids`: A list of comma-separated line IDs.

### Example

```sh
python -m FinalProjectSimulator 23-06-2024.00:00 30-06-2024.03:00 0.15 0.15 8 22064-1-#, 15025-1-0
```

### User Input
If the command-line arguments are not provided, the simulator will prompt the user to enter the required information.

## Additional Information
The simulator starts a different process for each line provided and runs each iteration on a separate thread.
The number of threads running in parallel equals the number of CPUs in the system.
Once the simulation ends, the analysis process starts for all iterations of the given simulation, and the combined results analysis is saved to the database.

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/) license.
You are free to use this work for personal purposes as long as you give appropriate credit, but you may not use it for commercial purposes without permission.

