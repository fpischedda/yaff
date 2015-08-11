import pyglet
from yaff.contrib.mixins import Bouncing


class Letter(Bouncing, pyglet.sprite.Sprite):

    def __init__(self, life_milliseconds, *args, **kwargs):
        self.life_milliseconds = life_milliseconds
        self.speed = 100
        super(Letter, self).__init__(*args, **kwargs)

    def die(self):

        self.delete()

    def on_update(self, dt):

        self.x += self.speed * self.direction[0] * dt
        self.y += self.speed * self.direction[1] * dt

        diff = self.update_direction(self.bounding_box())

        self.x -= diff[0]
        self.y -= diff[1]

        self.life_milliseconds -= dt
        if self.life_milliseconds <= 0:
            self.die()
            return False

        return True

    def bounding_box(self):

        return (self.x, self.y,
                self.x + self.width, self.y + self.height)
