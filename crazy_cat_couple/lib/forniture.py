from property import DynamicProperty


class Forniture:

    DEFAULT_OPTIONS = {
        'maintenance_cost': 0,
        'maintenance_seconds_left': 3600*24*365
    }

    def __init__(self, name, width, height, initial_cost, **options):
        self.name = name
        self.width = width
        self.height = height
        self.initial_cost = initial_cost

        opts = dict(Forniture.DEFAULT_OPTIONS, **options)
        self.maintenance_cost = opts['maintenance_cost']

        msl = opts['maintenance_seconds_left']
        self.properties = {
            'cleanness': DynamicProperty(name='cleanness',
                                         initial_value=100,
                                         min_value=0,
                                         max_value=100,
                                         decay_by_sec=0.001,
                                         gain_by_sec=0.1),
            'maintenance_seconds_left': DynamicProperty(name='msl',
                                                        initial_value=msl,
                                                        min_value=0,
                                                        max_value=msl,
                                                        decay_by_sec=1,
                                                        gain_by_sec=10)
        }

    def update(self, dt):
        for p in self.properties.values():
            p.update(dt)
