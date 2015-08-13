import pyglet


class Explosion(pyglet.sprite.Sprite):

    def __init__(self, x, y, scale, *args, **kwargs):

        super(Explosion, self).__init__(*args, **kwargs)

        self.x = x
        self.y = y
        self.scale = scale

    def on_animation_end(self):
        self.delete()
