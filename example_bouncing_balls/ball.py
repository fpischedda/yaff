import pyglet
from yaff.contrib.mixins import Bouncing


class Ball(Bouncing, pyglet.sprite.Sprite):

    def on_update(self, dt):

        self.x += 120 * self.direction[0] * dt
        self.y += 120 * self.direction[1] * dt

        diff = self.update_direction(self.bounding_box())

        self.x -= diff[0]
        self.y -= diff[1]

    def bounding_box(self):

        return (self.x, self.y, self.x + self.width, self.y + self.height)
