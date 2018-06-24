import os.path
from yaff import app
from yaff.contrib.scenes import SplashScene
from .game_scene import GameScene


def create_startup_scene():
    return SplashScene(
        next_scene_class=GameScene,
        sound_file_path='sfx/example_loop.wav',
        sound_loop=True)


def run():
    # here the abs path is used because, if run using the yaff runner, it will
    # considered a relative path of the yaff.py script
    res_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'res'))
    app.run(create_startup_scene, additional_resource_path=res_path)
