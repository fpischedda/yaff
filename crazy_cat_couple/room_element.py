class RoomElement:

    DEFAULT_OPTIONS = {
        'maintenance_cost': 0
    }

    def __init__(self, initial_cost, **options):
        self.initial_cost = initial_cost

        opts = dict(RoomElement.DEFAULT_OPTIONS, **options)
        self.maintenance_cost = opts['maintenance_cost']

    def draw(self, window):
        pass

    def update(self, dt):
        pass
