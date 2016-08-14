import pyglet
from yaff.scene import Scene


class SplashScene(Scene):
    """
    This class provides a simple splash screen scene
    optional parameters:
    - splash_image_path: path to an image to show, if not specified
    res/images/splash.jpg will be used
    - next_scene_class: a class to be istantiated when the user press
    a key
    - sound_file_path: path to a suond file that will be played at the
    start of the scene
    - sound_loop: defulat False; if set to True, the specified sound will
    be played in loop
    """

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

        try:
            from pudb import set_trace
            set_trace()
            sound_loop_path = kwargs.pop('sound_file_path')
            sound = pyglet.resource.media(sound_loop_path,
                                          streaming=False)
            player = pyglet.media.Player()

            loop = kwargs.pop('sound_loop', False)
            if loop:
                looper = pyglet.media.SourceGroup(sound.audio_format, None)
                looper.loop = True
                looper.queue(sound)
                player.queue(looper)
            else:
                player.queue(sound)

            player.play()
            self.player = player
        except Exception as e:
            print('Sound loop exception: ', e)
            self.player = None

        super(SplashScene, self).__init__(*args, **kwargs)

        self.image = pyglet.resource.image(self.splash_image_path)

    def on_key_press(self, symbol, modifier):
        self.director.prepare_next_scene(self.next_scene_class)
        return True

    def on_draw(self, window):

        super(SplashScene, self).on_draw(window)
        self.image.blit(0, 0)
