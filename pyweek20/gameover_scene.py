import pyglet
from yaff.scene import Scene
from yaff.contrib.scenes import SplashScene


class GameOverScene(Scene):

    def __init__(self, points, *args, **kwargs):

        super(GameOverScene, self).__init__(*args, **kwargs)

        score_str = "Your score: {score}".format(score=points)
        self.points_label = pyglet.text.Label(score_str,
                                              x=320,
                                              y=240,
                                              anchor_x='center',
                                              anchor_y='center')

    def on_key_press(self, symbol, modifier):
        from game_scene import GameScene
        self.director.prepare_next_scene(SplashScene,
                                         next_scene_class=GameScene)

    def on_draw(self, window):
        super(GameOverScene, self).on_draw(window)
        self.points_label.draw()
