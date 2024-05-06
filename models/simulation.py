from datetime import datetime, timedelta


class Simulation:
    def __init__(
        self,
        id: str,
        line_id: str,
        start_time: datetime,
        end_time: datetime,
        express_rate: float,
        reporting_rate: float,
        started_at: datetime,
    ):
        self.id = id
        self.line_id = line_id
        self.start_time = start_time
        self.end_time = end_time
        self.express_rate = express_rate
        self.reporting_rate = reporting_rate
        self.started_at = started_at
        self.duration: timedelta = None
        self.success: bool = False

    def set_duration(self):
        self.duration = datetime.now() - self.started_at

    def set_success(self, success: bool):
        self.success = success
