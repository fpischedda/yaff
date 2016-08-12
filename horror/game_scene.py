import random
import math
import pyglet
from yaff.scene import Scene
from .player import Player


class GameScene(Scene):

    def __init__(self, *args, **kwargs):

        super(GameScene, self).__init__(*args, **kwargs)

        image = pyglet.resource.image('res/images/sprites/sprite.png')

        self.batch = pyglet.graphics.Batch()

        self.player = Player(0, 0, image, batch=self.batch)

        self.background = pyglet.resource.image('res/images/bg/bg.jpg')

    def on_key_press(self, symbol, modifier):

        return True

    def on_update(self, dt):
        pass

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)

        self.background.blit(0, 0)
        self.batch.draw()
