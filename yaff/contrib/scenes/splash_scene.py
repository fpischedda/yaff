import pyglet
from yaff.scene import Scene


class SplashScene(Scene):

    splash_image_path = 'res/images/splash.jpg'
    next_scene_class = None

    def __init__(self, *args, **kwargs):

        try:
            self.splash_image_path = kwargs.pop('spash_image_path')
        except:
            pass

        try:
            self.next_scene_class = kwargs.pop('next_scene_class')
        except:
            pass

        super(SplashScene, self).__init__(*args, **kwargs)

        self.image = pyglet.resource.image(self.splash_image_path)
        self.image_alpha = 0

    def on_update(self, dt):
        self.image_alpha += dt
        if self.image_alpha > 1:
            self.image_alpha = 1

    def on_key_press(self, symbol, modifier):
        self.director.prepare_next_scene(self.next_scene_class)
        return True

    def on_draw(self, window):

        super(SplashScene, self).on_draw(window)
        self.image.blit(0, 0)
