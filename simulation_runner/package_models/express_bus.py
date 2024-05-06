from .bus import Bus


class ExpressBus(Bus):
    def __init__(self):
        super().__init__()
        self.pending_stops: list["Stop"] = []

    def add_stop(self, stop: "Stop") -> bool:
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


from .stop import Stop
