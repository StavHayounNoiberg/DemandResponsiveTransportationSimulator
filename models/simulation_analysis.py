class SimulationAnalysis:
    def __init__(self, id: int, simulation_ids: list[str], parameter: str, value: str):
        self.id = id
        self.simulation_ids = simulation_ids
        self.parameter = parameter
        self.value = value
