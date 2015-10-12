from property import DynamicProperty


class RoomElement:

    DEFAULT_OPTIONS = {
        'maintenance_cost': 0
    }

    def __init__(self, initial_cost, **options):
        self.initial_cost = initial_cost

        opts = dict(RoomElement.DEFAULT_OPTIONS, **options)
        self.maintenance_cost = opts['maintenance_cost']

        self.cleannes = DynamicProperty(name='cleannes',
                                        initial_value=100,
                                        min_value=0,
                                        max_value=100,
                                        decay_by_sec=0.001,
                                        gain_by_sec=0.1)

    def draw(self, window):
        pass

    def update(self, dt):
        pass
