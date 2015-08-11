import pyglet
from yaff.collidable import Collideable


class Bullet(Collideable, pyglet.sprite.Sprite):

    def __init__(self, speed, *args, **kwargs):

        self.speed = speed

        super(Bullet, self).__init__(*args, **kwargs)

    def on_update(self, dt):

        self.x += self.speed[0] * dt
        self.y += self.speed[1] * dt

        super(Bullet, self).on_update(dt)
