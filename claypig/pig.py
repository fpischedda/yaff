import pyglet
import math
import random
from yaff.contrib.mixins.linear_velocity import LinearVelocityMixin
from yaff.contrib.mixins.friction import FrictionMixin
from yaff.contrib.mixins.gravity import GravityMixin


class Pig(pyglet.sprite.Sprite, LinearVelocityMixin,
          FrictionMixin, GravityMixin):

    STATUS_ALIVE = 0
    STATUS_DEAD = 1

    START_LEFT = 1
    START_RIGHT = -1

    def __init__(self, start_side, *args, **kwargs):

        if start_side == self.START_LEFT:
            angle = random.randint(20, 70)
            start_x = 0
        else:
            start_x = 640
            angle = random.randint(110, 160)

        direction = (math.cos(angle),
                     math.sin(angle))

        speed = math.randint(20, 100)

        super(Pig, self).__init__(direction=direction,
                                  speed=speed,
                                  *args, **kwargs)

        self.set_position(start_x, 0)

        self.speed = 150
        self.status = self.STATUS_ALIVE

    def get_friction_direction(self):
        return (-self.direction[0],
                -self.direction[1])

    def set_image(self, image):
        self.image = image

    def set_animation(self, animation_name):
        self.image = self.animations[animation_name]

    def die(self):
        self.status = self.STATUS_DEAD
        self.direction[0] = 0
        self.direction[1] = 0

    def is_alive(self):
        return self.status == self.STATUS_ALIVE

    def on_update(self, dt):

        return super(Pig, self).update(dt)

    def bounding_box(self):

        return (self.x, self.y,
                self.x + self.width, self.y + self.height)
