import math
import pyglet
from yaff.contrib.mixins import Bouncing
from letter import Letter


class Ball(Bouncing, pyglet.sprite.Sprite):

    def __init__(self, tweet, *args, **kwargs):

        self.text = tweet['text']
        super(Ball, self).__init__(*args, **kwargs)

        self.scale = max(14, len(self.text)) / 140.0
        self.speed = 80 + min(tweet['retweet_count'] * 2, 50)

    def die(self):

        self.delete()
        return self.text

    def on_update(self, dt):

        self.x += self.speed * self.direction[0] * dt
        self.y += self.speed * self.direction[1] * dt

        diff = self.update_direction(self.bounding_box())

        self.x -= diff[0]
        self.y -= diff[1]

        return True

    def bounding_box(self):

        return (self.x, self.y, self.x + self.width, self.y + self.height)
