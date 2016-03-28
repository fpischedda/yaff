import pyglet
from yaff.contrib.mixins.linear_velocity import LinearVelocityMixin
from yaff.collidable import Collideable


class Bullet(Collideable, LinearVelocityMixin, pyglet.sprite.Sprite):

    def __init__(self, hit_damage, *args, **kwargs):

        self.hit_damage = hit_damage

        super(Bullet, self).__init__(*args, **kwargs)
