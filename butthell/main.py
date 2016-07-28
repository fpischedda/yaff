import os
import yaff.app
from yaff.contrib.scenes import SplashScene
from .game_scene import GameScene


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    yaff.app.run(SplashScene(next_scene_class=GameScene),
                 additional_resource_path=path)
