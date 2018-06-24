import pyglet
import bulletml
from yaff.scene import Scene
from yaff.contrib.bitmap_font import BitmapFont
from yaff.animation import load_animation
from .player import Player
from .bullet import Bullet
from .gameover_scene import GameOverScene


def load_animations(animations_def):

    return {
        anim: load_animation(data)
        for anim, data in animations_def.items()
    }


class GameScene(Scene):
    def __init__(self, *args, **kwargs):

        super(GameScene, self).__init__(*args, **kwargs)

        self.image = pyglet.resource.image('images/sprites/sprite.png')
        self.bullet_image = pyglet.resource.image('images/sprites/bullet.png')

        self.boundaries = [0, 0, 640, 480]

        self.setup_points()
        self.batch = pyglet.graphics.Batch()
        self.player = self.setup_player(self.batch)

        self.setup_bulletml(self.player)

        self.background = pyglet.resource.image('images/bg/bg1.jpg')

        self.sounds = {
            'pickup': pyglet.resource.media(
                'sfx/pickup.wav', streaming=False),
        }

    def setup_bulletml(self, target):
        with pyglet.resource.file('bulletml/boss.xml', 'rU') as f:
            doc = bulletml.BulletML.FromDocument(f)
            bullet = bulletml.Bullet.FromDocument(
                doc, 320, 240, target=target, rank=.05)
            self.bullets = [bullet]

    def setup_points(self):
        self.bitmap_font = BitmapFont('images/fonts/font.png', 5, 10)

        self.points = 0
        self.new_points = 0
        self.points_label = pyglet.text.Label(
            '0',
            font_name='Times New Roman',
            font_size=36,
            x=630,
            y=460,
            anchor_x='right',
            anchor_y='top')

    def setup_player(self, batch):
        player_animations = {
            'idle-right': {
                'loader': 'grid',
                'loader_params': {
                    'path': 'images/sprites/idle-right.png',
                    'rows': 1,
                    'cols': 6
                }
            },
            'idle-left': {
                'loader': 'grid',
                'loader_params': {
                    'path': 'images/sprites/idle-left.png',
                    'rows': 1,
                    'cols': 6
                }
            },
            'run-right': {
                'loader': 'grid',
                'loader_params': {
                    'path': 'images/sprites/run-right.png',
                    'rows': 1,
                    'cols': 4
                }
            },
            'run-left': {
                'loader': 'grid',
                'loader_params': {
                    'path': 'images/sprites/run-left.png',
                    'rows': 1,
                    'cols': 4
                }
            },
        }

        return Player(
            320,
            0,
            load_animations(player_animations),
            'idle-right',
            batch=batch)

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
            new_ones = []

            for b in self.bullets:
                new_ones.extend(b.step())

            self.bullets.extend(new_ones)

            self.bullets = [b for b in self.bullets if not b.finished]

        if self.player.on_update(dt) is False:
            self.director.prepare_next_scene(GameOverScene, self.new_points)

        self.update_points_label()

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)

        bg_x = -self.player.x
        bg_y = -self.player.y
        if bg_y < -240:
            bg_y = -240
        self.background.blit(bg_x, bg_y)
        self.batch.draw()
        for b in self.bullets:
            self.bullet_image.blit(b.x, b.y)
        self.points_label.draw()
