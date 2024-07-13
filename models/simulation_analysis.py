class SimulationAnalysis:
    def __init__(self, id: str, line_id: str, report_rate: float = 0.0, express_rate: float = 0.0, avg_travel_time_for_passenger: float = 0.0, avg_travel_time_for_bus: float = 0.0, avg_waiting_time_for_passenger: float = 0.0, rejected_passengers: float = 0.0, passengers_in_assignment: dict = {}):
        self.id = id
        self.line_id = line_id
        self.report_rate = report_rate
        self.express_rate = express_rate
        self.avg_travel_time_for_passenger = avg_travel_time_for_passenger
        self.avg_travel_time_for_bus = avg_travel_time_for_bus
        self.avg_waiting_time_for_passenger = avg_waiting_time_for_passenger
        self.rejected_passengers = rejected_passengers
        self.passengers_in_assignment = passengers_in_assignment
