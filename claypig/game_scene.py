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

        aim_image = pyglet.resource.image('res/images/sprites/aim.png')
        pig_image = pyglet.resource.image('res/images/ui/pig.png')

        self.batch = pyglet.graphics.Batch()

        self.aim = pyglet.sprite.Sprite(aim_image, x=100, y=0,
                                        batch=self.batch)

        self.body = pyglet.sprite.Sprite(pig_image, x=100, y=0,
                                         batch=self.batch)

        self.background = pyglet.resource.image('res/images/bg/bg.jpg')

    def on_update(self, dt):
        self.pig.update(dt)

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)

        self.background.blit(0, 0)
        self.batch.draw()
