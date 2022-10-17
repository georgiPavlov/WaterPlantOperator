class Status:

    def __init__(self, watering_status, message):
        self.watering_status = watering_status
        self.message = message


MESSAGE_INSUFFICIENT_WATER = "[Insufficient water in the container]"
MESSAGE_SUCCESS_MOISTURE = "[Plant successfully watered with moisture plan]"
MESSAGE_SUCCESS_TIMER = "Plant successfully watered with timer plan]"
MESSAGE_INVALID_PLAN = "[Invalid plan]"
MESSAGE_DELETED_PLAN = "[Watering plan deleted]"
MESSAGE_SUFFICIENT_WATER = "[Sufficient water in the container]"
MESSAGE_PLAN_CONDITION_NOT_MET = "[Plan condition not met]"
MESSAGE_BASIC_PLAN_SUCCESS = "[Successful watering of plant]"
HEALTH_CHECK = "healthcheck"

