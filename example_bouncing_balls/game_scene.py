import random
import math
import pyglet
from yaff.scene import Scene
from ball import Ball


def randomize_ball(boundaries, image, batch):
    angle = random.randint(0, 360) * 3.14 / 360
    direction = [math.cos(angle), math.sin(angle)]
    speed = random.randint(50, 200)
    b = Ball(boundaries, direction, speed, image, batch=batch)
    b.x = random.randint(30, 600)
    b.y = random.randint(30, 400)

    return b


class GameScene(Scene):

    def __init__(self, *args, **kwargs):

        super(GameScene, self).__init__(*args, **kwargs)

        image = pyglet.resource.image('res/images/sprites/sprite.png')

        self.boundaries = [0, 0, 640, 480]

        self.batch = pyglet.graphics.Batch()
        self.balls = [randomize_ball(self.boundaries, image, self.batch)
                      for _ in range(1000)]

        self.background = pyglet.resource.image('res/images/bg/bg.jpg')

    def on_key_press(self, symbol, modifier):
        if symbol == pyglet.window.key.M:
            self.boundaries[0] += 10
            self.boundaries[1] += 10
            self.boundaries[2] -= 10
            self.boundaries[3] -= 10

        if symbol == pyglet.window.key.N:
            self.boundaries[0] -= 10
            self.boundaries[1] -= 10
            self.boundaries[2] += 10
            self.boundaries[3] += 10

        return True

    def on_update(self, dt):
        for b in self.balls:
            b.on_update(dt)

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)

        self.background.blit(0, 0)
        self.batch.draw()
