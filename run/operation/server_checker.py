
class IServerCheckerInterface:

    def check_for_new_plan(self):
        pass

    def send_result(self):
        pass

    def show(self):
        raise Exception("NotImplementedException")


class ServerCheckerInterface(IServerCheckerInterface):
    def __init__(self):
        IServerCheckerInterface.__init__(self)


