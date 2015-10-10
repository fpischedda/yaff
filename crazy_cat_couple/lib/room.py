import pyglet


class Room:

    def __init__(self):
        self.background = pyglet.image.load()
        self.cleaness = 100
        self.cleaness_reduction_per_second = 0.01

        self.elements = []

    def draw(self, window):

        window.draw(self.background)

    def update(self, dt):

        self.cleaness -= self.cleaness_reduction_per_second * dt

        for e in self.elements:
            e.update(dt)
