import pyglet
from yaff.contrib.mixins import BouncingMixin
from yaff.contrib.mixins import LinearVelocityMixin


class Ball(BouncingMixin, LinearVelocityMixin,
           pyglet.sprite.Sprite):

    def on_update(self, dt):

        LinearVelocityMixin.on_update(self, dt)

        diff = self.check_boundaries(self.direction,
                                     self.bounding_box())

        self.x -= diff[0]
        self.y -= diff[1]

        if diff[0] != 0:
            self.direction[0] *= -1

        if diff[1] != 0:
            self.direction[1] *= -1

    def bounding_box(self):

        return (self.x, self.y, self.x + self.width, self.y + self.height)
