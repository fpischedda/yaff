from yaff import app
from yaff.contrib.scenes import SplashScene
from .game_scene import GameScene


if __name__ == '__main__':
    app.run(SplashScene(next_scene_class=GameScene,
                        splash_image_path='res/images/splash.png',
                        sound_file_path='res/sfx/girl_cry.ogg',
                        sound_loop=True))
