from yaff import app
from yaff.contrib.scenes import SplashScene
from .game_scene import GameScene


def run():
    app.run(SplashScene(next_scene_class=GameScene,
                        sound_file_path='res/sfx/example_loop.wav',
                        sound_loop=True))
