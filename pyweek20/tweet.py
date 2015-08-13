import pyglet
import settings


class Tweet(pyglet.sprite.Sprite):

    def __init__(self, tweet, direction, animations, *args, **kwargs):

        self.text = tweet['text']
        speed_variance = min(
            tweet['retweet_count'] * 2 + tweet['friends_count'] // 2, 100)
        speed = settings.TWEET_START_SPEED + speed_variance
        self.direction = [direction[0] * speed,
                          direction[1] * speed]

        self.elasticity = settings.TWEET_ELASTICITY

        if direction[0] > 0:
            anim = animations['bird-right']
        else:
            anim = animations['bird-left']

        self.animations = animations
        super(Tweet, self).__init__(anim, *args, **kwargs)
        self.scale = max(70, len(self.text)) / 140.0

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
                self.image = self.animations['bird-left']
        elif self.direction[0] < 0:
            if self.x < 0:
                self.x = -self.x // 2
                self.direction[0] = -self.direction[0]
                self.image = self.animations['bird-right']

        return True

    def bounding_box(self):

        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def collide(self, bbox):
        b = self.bounding_box()

        if b[0] <= bbox[2] and b[1] <= bbox[3] \
                and b[2] >= bbox[0] and b[3] >= bbox[1]:
            return True

        return False
