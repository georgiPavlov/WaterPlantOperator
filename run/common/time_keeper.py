import datetime


class TimeKeeper:
    def __init__(self, current_time):
        self.current_time = current_time
        self.time_last_watered = None

    def set_current_time(self, updated_time):
        self.current_time = updated_time

    def set_time_last_watered(self, updated_time):
        self.time_last_watered = updated_time

    @staticmethod
    def get_current_time():
        now = datetime.datetime.now()
        return now.strftime("%I:%M %p")

    @staticmethod
    def get_time_from_time_string(time_string):
        return datetime.datetime.strptime(time_string, "%I:%M %p")


    @staticmethod
    def get_current_time_minus_delta(delta):
        now = datetime.datetime.now()
        time_change = datetime.timedelta(minutes=delta)
        time_with_delta = now - time_change
        return time_with_delta.strftime("%I:%M %p")
