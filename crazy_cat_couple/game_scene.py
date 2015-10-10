import settings
from yaff.scene import Scene
from gameover_scene import GameOverScene
from utils import load_grid_animation


class GameScene(Scene):

    def __init__(self, *args, **kwargs):

        super(GameScene, self).__init__(*args, **kwargs)

    def on_key_release(self, symbol, modifier):
        pass

    def on_key_press(self, symbol, modifier):
        return True

    def on_update(self, dt):
        pass

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)
