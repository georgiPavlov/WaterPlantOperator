from gpiozero import LightSensor


class Moisture(LightSensor):
    def __init__(self, pin=None, queue_len=5,
                 charge_time_limit=0.01, threshold=0.1,
                 partial=False, pin_factory=None):
        super(Moisture, self).__init__(pin,
                                       threshold=threshold,
                                       queue_len=queue_len,
                                       charge_time_limit=charge_time_limit,
                                       pin_factory=pin_factory)

    def wait_for_dry(self):
        return super(Moisture, self).wait_for_light

    def wait_for_wet(self):
        return super().wait_for_dark

    def when_dry(self):
        return super().when_light

    def when_wet(self):
        return super().when_dark

    def is_dry(self):
        return super().is_active
