import pyglet
from yaff.conf import settings
from yaff.scene import Scene
from yaff.utils import load_grid_animation
from yaff.contrib.bitmap_font import BitmapFont
from player import Player
from gameover_scene import GameOverScene


def load_animation(animation_data):
    func = settings.LOADERS[animation_data['loader']]

    params = animation_data['parameters']
    if isinstance(params, dict):
        return func(**params)
    elif isinstance(params, list):
        return func(*params)
    else:
        return func()


def load_animations(animations_def):

    return {anim: load_animation
            for anim, data in animations_def.items()}


class GameScene(Scene):

    def __init__(self, *args, **kwargs):

        super(GameScene, self).__init__(*args, **kwargs)

        self.image = pyglet.resource.image('res/images/sprites/sprite.png')

        self.boundaries = [0, 0, 640, 480]

        self.bitmap_font = BitmapFont('res/images/fonts/font.png', 5, 10)
        self.batch = pyglet.graphics.Batch()

        self.points = 0
        self.new_points = 0
        self.points_label = pyglet.text.Label('0',
                                              font_name='Times New Roman',
                                              font_size=36,
                                              x=630, y=460,
                                              anchor_x='right',
                                              anchor_y='top')

        player_animations = {
            'idle-right': {
                'loader': 'grid',
                'loader_params': {
                    'path': 'res/images/sprites/idle-right.png',
                    'rows': 1,
                    'cols': 6
                }
            },
            'idle-left': {
                'loader': 'grid',
                'loader_params': {
                    'path': 'res/images/sprites/idle-left.png',
                    'rows': 1,
                    'cols': 6
                }
            },
            'run-right': {
                'loader': 'grid',
                'loader_params': {
                    'path': 'res/images/sprites/run-right.png',
                    'rows': 1,
                    'cols': 4
                }
            },
            'run-left': {
                'loader': 'grid',
                'loader_params': {
                    'path': 'res/images/sprites/run-left.png',
                    'rows': 1,
                    'cols': 4
                }
            },
            'rolling-right': load_grid_animation(
                'res/images/sprites/rolling-right.png',
                1, 3),
            'rolling-left': load_grid_animation(
                'res/images/sprites/rolling-left.png',
                1, 3),
            'dying': load_grid_animation(
                'res/images/sprites/dying.png',
                1, 9, 0.12),
        }

        self.player = Player(320, 0, player_animations,
                             player_animations['idle-right'],
                             batch=self.batch)

        self.bird_animations = {
            'bird-right': load_grid_animation(
                'res/images/sprites/bird-right.png',
                1, 7),
            'bird-left': load_grid_animation(
                'res/images/sprites/bird-left.png',
                1, 7),
        }
        self.background = pyglet.resource.image('res/images/bg/bg1.jpg')

        self.explosion_animation = load_grid_animation(
            'res/images/sprites/explosion.png', 1, 6
        )

        self.sounds = {
            'pickup': pyglet.media.load('res/sfx/pickup.wav',
                                        streaming=False),
        }

    def on_key_release(self, symbol, modifier):

        if symbol == pyglet.window.key.A:
            self.player.set_key_released(Player.DIRECTION_LEFT)
        elif symbol == pyglet.window.key.D:
            self.player.set_key_released(Player.DIRECTION_RIGHT)

        if symbol == pyglet.window.key.W:
            self.player.set_key_released(Player.DIRECTION_UP)

    def on_key_press(self, symbol, modifier):

        if symbol == pyglet.window.key.A:
            self.player.set_key_pressed(Player.DIRECTION_LEFT)
        elif symbol == pyglet.window.key.D:
            self.player.set_key_pressed(Player.DIRECTION_RIGHT)

        if symbol == pyglet.window.key.W:
            self.player.set_key_pressed(Player.DIRECTION_UP)

        return True

    def update_points_label(self):

        if self.points < self.new_points:
            self.points += 10
            self.points_label.text = str(self.points)

    def on_update(self, dt):

        if self.player.is_alive():
            self.check_letter_collisions()
            self.check_tweet_collisions()

        if self.player.on_update(dt) is False:
            self.director.prepare_next_scene(GameOverScene, self.new_points)

        self.update_points_label()

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)

        bg_x = -self.player.x
        bg_y = -self.player.y
        if bg_y < - 240:
            bg_y = -240
        self.background.blit(bg_x, bg_y)
        self.batch.draw()
        self.points_label.draw()
