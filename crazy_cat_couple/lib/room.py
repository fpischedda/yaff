from .property import DynamicProperty


class Room:

    def __init__(self, name, width, height):
        self.name = name

        self.wall_type = 'static'
        self.wall_variant = 'concrete1'

        self.width = width
        self.height = height
        self.properties = {
            'cleanness': DynamicProperty(name='cleanness',
                                         initial_value=100,
                                         decay_by_sec=0.001,
                                         min_value=0,
                                         gain_by_sec=100,
                                         max_value=100,
                                         decaying=True)
        }

        self.elements = []

    def update(self, dt):

        for p in self.properties.values():
            p.update(dt)

        for e in self.elements:
            e.update(dt)
