class SimulationResult:
    def __init__(self, id: int, simulation_id: int, result_type: str, value: str):
        self.id = id
        self.simulation_id = simulation_id
        self.result_type = result_type
        self.value = value
