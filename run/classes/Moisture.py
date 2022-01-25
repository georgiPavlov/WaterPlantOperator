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
Moisture.wait_for_dry=Moisture.wait_for_light
Moisture.wait_for_wet=Moisture.wait_for_dark
Moisture.when_dry=Moisture.when_light
Moisture.when_wet=Moisture.when_dark
