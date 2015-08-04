import pyglet
from yaff.scene import Scene


class GameScene(Scene):

    def __init__(self, *args, **kwargs):

        super(GameScene, self).__init__(*args, **kwargs)

        image = pyglet.resource.image('res/images/sprites/sprite.png')
        self.sprite = pyglet.sprite.Sprite(image)
        self.background = pyglet.resource.image('res/images/bg/bg.jpg')

    def on_key_press(self, symbol, modifier):
        self.sprite.x += 10
        self.sprite.y += 10
        return True

    def on_update(self, dt):
        self.sprite.x += 30 * dt
        self.sprite.y += 30 * dt

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)

        self.background.blit(0, 0)
        self.sprite.draw()
