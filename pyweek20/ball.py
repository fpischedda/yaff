import math
import pyglet
from yaff.contrib.mixins import Bouncing


class Ball(Bouncing, pyglet.sprite.Sprite):

    def __init__(self, tweet, *args, **kwargs):

        self.tweet = tweet
        super(Ball, self).__init__(*args, **kwargs)

        self.scale = max(14, len(tweet['text'])) / 140.0
        self.speed = 80 + min(tweet['retweet_count'] * 2, 50)
        self.respawn = min(tweet['friends_count'] // 100, 20)

    def die(self):
        if self.respawn <= 0:
            return []

        respawn_opts = {'text': 'R',
                        'friends_count': 0,
                        'retweet_count': 0
                        }
        balls = []
        angle = 0
        angle_diff = 360 / self.respawn
        for i in range(self.respawn):
            direction = [math.cos(angle), math.sin(angle)]
            b = Ball(respawn_opts,
                     self.boundaries,
                     direction,
                     self.image,
                     batch=self.batch)
            b.x = self.x
            b.y = self.y

            balls.append(b)
            angle += angle_diff

        self.delete()
        return balls

    def on_update(self, dt):

        self.x += self.speed * self.direction[0] * dt
        self.y += self.speed * self.direction[1] * dt

        diff = self.update_direction(self.bounding_box())

        self.x -= diff[0]
        self.y -= diff[1]

    def bounding_box(self):

        return (self.x, self.y, self.x + self.width, self.y + self.height)
