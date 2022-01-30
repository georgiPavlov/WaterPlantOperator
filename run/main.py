from run.common import time_keeper as TK
from sensor.relay import Relay
from sensor.moisture_sensor import Moisture
import time

# WATERING_TIME must be in "00:00:00 PM" format
WATERING_TIME = '08:22:40 PM'
SECONDS_TO_WATER = 5000
RELAY = Relay(12, False)
moisture = Moisture(4, charge_time_limit=0.2, threshold=0.6)


def water_plant(relay, seconds):
    relay.on()
    print("Plant is being watered!")
    time.sleep(seconds)
    print("Watering is finished!")
    relay.off()

def main():
    moisture.wait_for_dry()
    time_keeper = TK.TimeKeeper(TK.TimeKeeper.get_current_time())
    print("current time " +  TK.TimeKeeper.get_current_time())
    water_plant(RELAY, SECONDS_TO_WATER)
    time_keeper.set_time_last_watered(TK.TimeKeeper.get_current_time())
    print("\nPlant was last watered at {}".format(time_keeper.time_last_watered))
    #time_keeper = TK.TimeKeeper(TK.TimeKeeper.get_current_time())
   # if(time_keeper.current_time == WATERING_TIME):
    #    water_plant(RELAY, SECONDS_TO_WATER)
     #   time_keeper.set_time_last_watered(TK.TimeKeeper.get_current_time())
      #  print("\nPlant was last watered at {}".format(time_keeper.time_last_watered))
        # send_last_watered_email(time_keeper.time_last_watered)

# schedule.every().friday.at("12:00").do(send_check_water_level_email)

while True:
    # schedule.run_pending()
    time.sleep(1)
    print(moisture.value)

    #for d in moisture.values:
     #   print(d)
        # moisture.when_dry = print("dry")
        # moisture.when_wet = print ("wet")
      #  moisture.wait_for_wet
        #print(moisture.wait_for_dry)
        #time.sleep(2)
    main()
