class SimulationAnalysis:
    def __init__(self,
                 id: str,
                 simulations_ids: list[str],
                 line_id: str,
                 report_rate: float = 0.0,
                 express_rate: float = 0.0,
                 avg_bus_count: float = 0.0,
                 avg_passengers_count: float = 0.0,
                 avg_bus_travel_time: float = 0.0,
                 avg_passenger_travel_time: float = 0.0, 
                 avg_passenger_waiting_time: float = 0.0,
                 rejected_passengers: float = 0.0,
                 passengers_in_assignment: dict = {}):
        self.id = id
        self.simulations_ids = simulations_ids
        self.line_id = line_id
        self.report_rate = report_rate
        self.express_rate = express_rate
        self.avg_bus_count = avg_bus_count
        self.avg_passengers_count = avg_passengers_count
        self.avg_bus_travel_time = avg_bus_travel_time
        self.avg_passenger_travel_time = avg_passenger_travel_time
        self.avg_passenger_waiting_time = avg_passenger_waiting_time
        self.rejected_passengers = rejected_passengers
        self.passengers_in_assignment = passengers_in_assignment
