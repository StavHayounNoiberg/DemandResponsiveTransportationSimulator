from models.bus import Bus
from models.stop import Stop
from line_manager import LineManager


class ExpressBus(Bus):
    def __init__(self, line_manager: LineManager):
        super().__init__(line_manager)
        self.pending_stops: list[Stop] = []

    def add_stop(self, stop: Stop) -> bool:
        try:
            self.pending_stops.append(stop)
            return True
        except Exception as e:
            print(e)
            return False

    def clear_pending_stops(self) -> bool:
        try:
            self.pending_stops.clear()
            return True
        except Exception as e:
            print(e)
            return False
