import random
import math
import pyglet
from yaff.scene import Scene
from yaff.animation import load_animation
from .tweet import Tweet
from .player import Player
from .explosion import Explosion
from .bitmap_font import BitmapFont
from .gameover_scene import GameOverScene
from . import settings
from .utils import spawn_letters


def randomize_starting_point():
    if random.random() >= 0.5:
        return (math.radians(random.randint(45, 80)), 40, 0)

    return (math.radians(random.randint(100, 135)), 600, 0)


def randomize_tweet(animations, batch, msg):

    angle, x, y = randomize_starting_point()

    direction = [math.cos(angle), math.sin(angle)]
    b = Tweet(msg, animations, direction,
              gravity=settings.GRAVITY,
              batch=batch)
    b.x = x
    b.y = y

    return b


def load_animations(animations_def):

    return {anim: load_animation(data)
            for anim, data in animations_def.items()}


class GameScene(Scene):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.image = pyglet.resource.image('images/sprites/sprite.png')

        self.tweet_timeout = 1.5

        self.boundaries = [0, 0, 640, 480]

        self.bitmap_font = BitmapFont('images/fonts/font.png', 5, 10)
        self.batch = pyglet.graphics.Batch()
        self.tweets = []
        self.letters = []

        self.points = 0
        self.new_points = 0
        self.timeout_label = pyglet.text.Label('0',
                                               font_name='Times New Roman',
                                               font_size=36,
                                               x=630, y=360,
                                               anchor_x='right',
                                               anchor_y='top')
        self.points_label = pyglet.text.Label('0',
                                              font_name='Times New Roman',
                                              font_size=36,
                                              x=630, y=460,
                                              anchor_x='right',
                                              anchor_y='top')

        player_animations = load_animations({
            'idle-right': {
                'loader': 'grid',
                'parameters':
                ['images/sprites/idle-right.png', 1, 6]
            },
            'idle-left': {
                'loader': 'grid',
                'parameters':
                ['images/sprites/idle-left.png',
                 1, 6]},
            'run-right': {
                'loader': 'grid',
                'parameters':
                ['images/sprites/run-right.png',
                 1, 4]},
            'run-left': {
                'loader': 'grid',
                'parameters':
                ['images/sprites/run-left.png',
                 1, 4]},
            'rolling-right': {
                'loader': 'grid',
                'parameters':
                ['images/sprites/rolling-right.png',
                 1, 3]},
            'rolling-left': {
                'loader': 'grid',
                'parameters':
                ['images/sprites/rolling-left.png',
                 1, 3]},
            'dying': {
                'loader': 'grid',
                'parameters':
                ['images/sprites/dying.png',
                 1, 9, 0.12]},
        })

        self.player = Player(320, 0, player_animations,
                             player_animations['idle-right'],
                             batch=self.batch)

        self.bird_animations = load_animations({
            'bird-right': {
                'loader': 'grid',
                'parameters':
                ['images/sprites/bird-right.png',
                 1, 7]},
            'bird-left': {
                'loader': 'grid',
                'parameters':
                ['images/sprites/bird-left.png',
                 1, 7]},
        })
        self.background = pyglet.resource.image('images/bg/bg1.jpg')

        self.explosion_animation = load_animation({
                'loader': 'grid',
                'parameters':
                ['images/sprites/explosion.png', 1, 6]})

        self.sounds = {
            'pickup': pyglet.resource.media('sfx/pickup.wav',
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

    def add_tweets(self):

        for i in range(10):
            msg = "Boo" + "O" * i + "M!!!"
            self.tweets.append(randomize_tweet(self.bird_animations,
                                               self.batch,
                                               msg))

    def check_tweet_collisions(self):
        bbox = self.player.bounding_box()

        collisions = [t for t in self.tweets if t.collide(bbox)]

        if self.player.jumping:
            for c in collisions:
                self.tweets.remove(c)
                new_letters = spawn_letters(self.bitmap_font, c.die(),
                                            c.x, c.y, self.batch,
                                            self.boundaries)
                self.letters.extend(new_letters)
                Explosion(c.x, c.y, c.scale,
                          self.explosion_animation, batch=self.batch)
        elif len(collisions) > 0:
            self.player.die()

    def check_letter_collisions(self):
        bbox = self.player.bounding_box()

        collisions = [l for l in self.letters if l.collide(bbox)]

        for c in collisions:
            self.letters.remove(c)
            c.die()
            self.new_points += settings.LETTER_POINTS

        # if len(collisions) > 0:
            # self.sounds['pickup'].play()

    def update_points_label(self):

        if self.points < self.new_points:
            self.points += 10
            self.points_label.text = str(self.points)

    def on_update(self, dt):
        self.tweet_timeout -= dt
        if self.tweet_timeout < 0:
            self.tweet_timeout = 1.5 + 1.5 * random.random()
            self.add_tweets()

        for t in self.tweets:
            t.on_update(dt)
        self.timeout_label.text = f'{self.tweet_timeout:.2f}'

        if self.player.is_alive():
            self.check_letter_collisions()
            self.check_tweet_collisions()

        to_remove = [l for l in self.letters if l.on_update(dt) is False]
        for r in to_remove:
            self.letters.remove(r)

        if self.player.on_update(dt) is False:
            self.director.prepare_next_scene(GameOverScene, self.new_points)

        self.update_points_label()

    def on_draw(self, window):

        super().on_draw(window)

        bg_x = -self.player.x
        bg_y = -self.player.y
        if bg_y < - 240:
            bg_y = -240
        self.background.blit(bg_x, bg_y)
        self.batch.draw()
        self.points_label.draw()
        self.timeout_label.draw()
