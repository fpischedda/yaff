"""
an Action is a unit of work that can be applied to
an entity to modify its state over time;
an Action has a state choosed from:
* IDLE,
* RUNNING
* FINISHED

an Action can react to the following events:
* on_start(self)
* on_update(self, dt): return True when still running otherwise False
* on_finish(self)

the Action contructor at least accepts a target object and:
* a start_callback called when the action effectively starts
* a finish callback callend when the action finish its life cycle
callbacks receives the action that generated it and the target object
"""


class BaseAction(object):

    STATUS_IDLE = 0
    STATUS_RUNNING = 1
    STATUS_FINISHED = 2

    def __init__(self, target, start_callback=None, finish_callback=None):
        self.target = target
        self.start_callback = start_callback
        self.finish_callback = finish_callback
        self.status = self.STATUS_IDLE

    def start(self):
        self.status = self.STATUS_IDLE
        self.on_start()

    def stop(self):
        self.status = self.STATUS_FINISHED
        self.on_finish()

    def on_start(self):
        if self.start_callback:
            self.start_callback(self, self.target)

    def on_finish(self):
        if self.finish_callback:
            self.finish_callback(self, self.target)

    def on_update(self, dt):
        self.finish()
        return False
