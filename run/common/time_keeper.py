import datetime

TIME_FORMAT = "%H:%M"


class TimeKeeper:

    def __init__(self, current_time):
        self.current_time = current_time
        self.time_last_watered = None
        self.date_last_watered = None

    def set_current_time(self, updated_time):
        self.current_time = updated_time

    def set_time_last_watered(self, updated_time):
        self.time_last_watered = updated_time

    def set_date_last_watered(self, date_last_watered):
        self.date_last_watered = date_last_watered

    @staticmethod
    def get_current_time():
        now = datetime.datetime.now()
        return now.strftime(TIME_FORMAT)

    @staticmethod
    def get_current_date():
        return datetime.date.today()

    @staticmethod
    def get_time_from_time_string(time_string):
        return datetime.datetime.strptime(time_string, TIME_FORMAT).strftime(TIME_FORMAT)

    @staticmethod
    def get_current_time_minus_delta(delta):
        now = datetime.datetime.now()
        time_change = datetime.timedelta(minutes=delta)
        time_with_delta = now - time_change
        return time_with_delta.strftime(TIME_FORMAT)
