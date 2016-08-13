from yaff import app
from yaff.contrib.scenes import SplashScene
from .game_scene import GameScene


if __name__ == '__main__':
    app.run(SplashScene(next_scene_class=GameScene))