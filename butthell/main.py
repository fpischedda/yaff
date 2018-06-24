import os
import yaff.app
from yaff.contrib.scenes import SplashScene
from .game_scene import GameScene


def create_splash_scene():
    return SplashScene(next_scene_class=GameScene)


def run():
    res_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'res'))
    yaff.app.run(create_splash_scene, additional_resource_path=res_path)
