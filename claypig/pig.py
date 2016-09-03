import pyglet
import math
import random
from yaff.contrib.mixins.linear_velocity import LinearVelocityMixin
from yaff.contrib.mixins.gravity import GravityMixin


class Pig(pyglet.sprite.Sprite, LinearVelocityMixin,
          GravityMixin):

    STATUS_ALIVE = 0
    STATUS_DEAD = 1

    START_LEFT = 0
    START_RIGHT = 1

    def __init__(self, *args, **kwargs):

        super(Pig, self).__init__(direction=(0, 0),
                                  speed=0,
                                  *args, **kwargs)

        self.speed = 150
        self.status = self.STATUS_ALIVE

    def spawn(self, side, speed):
        if side == self.START_LEFT:
            angle = random.randint(20, 70)
            start_x = 0
        else:
            start_x = 640
            angle = random.randint(110, 160)

        self.direction = (math.cos(angle),
                          math.sin(angle))

        self.speed = math.randint(20, 100)
        self.set_position(start_x, 0)

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
