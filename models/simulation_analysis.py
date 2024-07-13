class SimulationAnalysis:
    def __init__(self,
                 id: str,
                 line_id: str,
                 report_rate: float = 0.0,
                 express_rate: float = 0.0,
                 avg_passenger_travel_time: float = 0.0, 
                 avg_passenger_travel_time_percent: float = 0.0,
                 avg_bus_travel_time: float = 0.0,
                 avg_bus_travel_time_percent: float = 0.0,
                 avg_passenger_waiting_time: float = 0.0,
                 avg_passenger_waiting_time_percent: float = 0.0,
                 rejected_passengers: float = 0.0,
                 passengers_in_assignment: dict = {}):
        self.id = id
        self.line_id = line_id
        self.report_rate = report_rate
        self.express_rate = express_rate
        self.avg_passenger_travel_time = avg_passenger_travel_time
        self.avg_passenger_travel_time_percent = avg_passenger_travel_time_percent
        self.avg_bus_travel_time = avg_bus_travel_time
        self.avg_bus_travel_time_percent = avg_bus_travel_time_percent
        self.avg_passenger_waiting_time = avg_passenger_waiting_time
        self.avg_passenger_waiting_time_percent = avg_passenger_waiting_time_percent
        self.rejected_passengers = rejected_passengers
        self.passengers_in_assignment = passengers_in_assignment
