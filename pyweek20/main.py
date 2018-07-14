import os.path
from yaff import app
from yaff.contrib.scenes import SplashScene
from .game_scene import GameScene


class MainSplashScene(SplashScene):
    next_scene_class = GameScene


def run():
    # here the abs path is used because, if run using the yaff runner, it will
    # considered a relative path of the yaff.py script
    res_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'res'))
    app.run(MainSplashScene, additional_resource_path=res_path)
