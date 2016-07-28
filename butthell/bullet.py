import pyglet


class Bullet(pyglet.sprite.Sprite):

    def __init__(self, hit_damage, *args, **kwargs):

        self.hit_damage = hit_damage
        image = pyglet.resource.image('res/images/sprites/sprite.png')

        super(Bullet, self).__init__(image, *args, **kwargs)
