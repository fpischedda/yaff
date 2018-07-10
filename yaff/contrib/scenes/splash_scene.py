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
    - sound_loop: default False; if set to True, the specified sound will
    be played in loop
    """

    splash_image_path = 'images/splash.jpg'
    sound_file_path = None
    sound_loop = False
    next_scene_class = None

    def __init__(self, *args, **kwargs):

        self.splash_image_path = kwargs.pop('splash_image_path',
                                            self.splash_image_path)

        self.next_scene_class = kwargs.pop('next_scene_class',
                                           self.next_scene_class)

        sound_file_path = kwargs.pop('sound_file_path',
                                     self.sound_file_path)
        loop = kwargs.pop('sound_loop', self.sound_loop)
        if sound_file_path:
            try:
                sound = pyglet.resource.media(sound_file_path,
                                              streaming=not loop)
                player = pyglet.media.Player()

                if loop:
                    looper = pyglet.media.SourceGroup(sound.audio_format, None)
                    looper.loop = True
                    looper.queue(sound)
                    player.queue(looper)
                else:
                    player.queue(sound)

                # player.play()
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
