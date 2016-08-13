import random
import math
import pyglet
from yaff.scene import Scene
from .player import Player


class GameScene(Scene):

    KEY_MOVEMENT_MAPPING = {
        pyglet.window.key.A: Player.DIRECTION_LEFT,
        pyglet.window.key.D: Player.DIRECTION_RIGHT,
        pyglet.window.key.W: Player.DIRECTION_UP,
        pyglet.window.key.S: Player.DIRECTION_DOWN,
    }
    def __init__(self, *args, **kwargs):

        super(GameScene, self).__init__(*args, **kwargs)

        image = pyglet.resource.image('res/images/sprites/sprite.png')

        self.batch = pyglet.graphics.Batch()

        self.player = Player(0, 0, image, batch=self.batch)

        body_img = pyglet.resource.image('res/images/ui/body.png')
        self.body = pyglet.sprite.Sprite(body_img, x=100, y=0,
                                         batch=self.batch)
        self.body.scale = 0.3

        self.background = pyglet.resource.image('res/images/bg/bg.jpg')

    def on_key_press(self, symbol, modifier):

        if symbol in self.KEY_MOVEMENT_MAPPING:
            self.player.on_key_pressed(self.KEY_MOVEMENT_MAPPING[symbol])
            return True
        return False

    def on_key_release(self, symbol, modifier):

        if symbol in self.KEY_MOVEMENT_MAPPING:
            self.player.on_key_released(self.KEY_MOVEMENT_MAPPING[symbol])
            return True
        return False

    def on_update(self, dt):
        self.player.on_update(dt)

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)

        self.background.blit(0, 0)
        self.batch.draw()
