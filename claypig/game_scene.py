import random
import pyglet
from yaff.scene import Scene
from .pig import Pig


class GameScene(Scene):

    def __init__(self, *args, **kwargs):

        super(GameScene, self).__init__(*args, **kwargs)

        aim_image = pyglet.resource.image('res/images/sprites/aim.png')
        pig_image = pyglet.resource.image('res/images/sprites/pig.png')

        self.batch = pyglet.graphics.Batch()

        self.aim = pyglet.sprite.Sprite(aim_image, x=100, y=0,
                                        batch=self.batch)

        self.pig = Pig(pig_image, x=100, y=0,
                       batch=self.batch)

        self.background = pyglet.resource.image('res/images/bg/bg.jpg')

    def spawn_pig(self):
        if random.randint(100) > 50:
            side = Pig.START_LEFT
        else:
            side = Pig.START_RIGTH
        self.pig.spaw(side)

    def on_update(self, dt):
        self.pig.on_update(dt)

    def on_mouse_motion(self, x, y, dx, dy):
        self.aim.set_position(x, y)

    def on_key_press(self, symbol, modifier):
        self.spawn_pig()

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)

        self.background.blit(0, 0)
        self.batch.draw()
