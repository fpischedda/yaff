import pyglet
import settings


class Tweet(pyglet.sprite.Sprite):

    def __init__(self, tweet, direction, *args, **kwargs):

        super(Tweet, self).__init__(*args, **kwargs)

        self.text = tweet['text']
        self.scale = max(14, len(self.text)) / 140.0
        speed = 80 + min(tweet['retweet_count'] * 2, 50)
        self.direction = [direction[0] * speed,
                          direction[1] * speed]

        self.elasticity = 0.8

    def die(self):

        self.delete()
        return self.text

    def apply_gravity(self, dt):
        self.direction[1] -= settings.GRAVITY * dt

    def on_update(self, dt):

        self.apply_gravity(dt)

        self.x += self.direction[0] * dt
        self.y += self.direction[1] * dt

        if self.y < 0:
            self.y = -self.y // 2
            self.direction[1] *= -self.elasticity

        if self.direction[0] > 0:
            if self.x > 640 - self.width:
                self.x = 640 - self.width
                self.direction[0] = -self.direction[0]
        elif self.direction[0] < 0:
            if self.x < 0:
                self.x = -self.x // 2
                self.direction[0] = -self.direction[0]

        return True

    def bounding_box(self):

        return (self.x, self.y, self.x + self.width, self.y + self.height)
