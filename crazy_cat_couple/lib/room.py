from property import DynamicProperty


class Room:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.properties = {
            'cleanness': DynamicProperty(name='cleanness',
                                         initial_value=100,
                                         decay_by_sec=0.001,
                                         min_value=0,
                                         gain_by_sec=100,
                                         max_value=100)
        }

        self.elements = []

    def update(self, dt):

        for p in self.properties.values():
            p.update(dt)

        for e in self.elements:
            e.update(dt)
