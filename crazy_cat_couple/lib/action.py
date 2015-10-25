class BaseAction:

    STATUS_IDLE = 0
    STATUS_RUNNING = 1
    STATUS_FINISHED = 2

    def __init__(self, name):

        self.status = BaseAction.STATUS_IDLE
