import pyglet
from yaff.contrib.mixins import BouncingMixin


class Letter(BouncingMixin, pyglet.sprite.Sprite):

    def __init__(self, life_milliseconds, *args, **kwargs):
        self.life_milliseconds = life_milliseconds
        self.speed = 120
        super(Letter, self).__init__(*args, **kwargs)
        self.scale = 2

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

    def collide(self, bbox):
        b = self.bounding_box()

        if b[0] <= bbox[2] and b[1] <= bbox[3] \
                and b[2] >= bbox[0] and b[3] >= bbox[1]:
            return True

        return False
