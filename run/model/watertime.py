class WaterTime:
    weekday: str
    time_water: str

    def __init__(self, weekday: str, time_water: str) -> None:
        self.weekday = weekday
        self.time_water = time_water
