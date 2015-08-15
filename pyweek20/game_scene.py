import random
import math
import pyglet
import queue
import threading
import settings
from yaff.scene import Scene
from tweet import Tweet
from player import Player
from explosion import Explosion
from bitmap_font import BitmapFont
from consumer import Consumer
from gameover_scene import GameOverScene
from utils import load_grid_animation
from utils import spawn_letters


def feeds_worker(message_queue):

    consumer = Consumer(settings.BROKER_URL, message_queue)

    try:
        consumer.start_consuming()
    except:
        consumer.close_connection()


def randomize_starting_point():
    if random.random() >= 0.5:
        return (math.radians(random.randint(45, 80)), 40, 0)

    return (math.radians(random.randint(100, 135)), 600, 0)


def randomize_tweet(animations, batch, msg):

    angle, x, y = randomize_starting_point()

    direction = [math.cos(angle), math.sin(angle)]
    b = Tweet(msg, direction, animations, batch=batch)
    b.x = x
    b.y = y

    return b


class GameScene(Scene):

    def __init__(self, *args, **kwargs):

        super(GameScene, self).__init__(*args, **kwargs)

        self.image = pyglet.resource.image('res/images/sprites/sprite.png')

        self.queue = queue.Queue()

        self.boundaries = [0, 0, 640, 480]

        self.bitmap_font = BitmapFont('res/images/fonts/font.png', 5, 10)
        self.batch = pyglet.graphics.Batch()
        self.tweets = []
        self.letters = []

        self.points = 0
        self.new_points = 0
        self.points_label = pyglet.text.Label('0',
                                               font_name='Times New Roman',
                                               font_size=36,
                                               x=630, y=460,
                                               anchor_x='right',
                                               anchor_y='top')

        player_animations = {
            'idle-right': load_grid_animation(
                'res/images/sprites/idle-right.png',
                1, 6),
            'idle-left': load_grid_animation(
                'res/images/sprites/idle-left.png',
                1, 6),
            'run-right': load_grid_animation(
                'res/images/sprites/run-right.png',
                1, 4),
            'run-left': load_grid_animation(
                'res/images/sprites/run-left.png',
                1, 4),
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

        self.start_feeds_thread()

    def start_feeds_thread(self):

        print("starting feed thread...")
        t = threading.Thread(target=feeds_worker, args=(self.queue,))
        t.daemon = True
        t.start()

        print("feed thread started...")
        self.thread = t

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

        while not self.queue.empty():
            msg = self.queue.get()
            self.tweets.append(randomize_tweet(self.bird_animations,
                                               self.batch,
                                               msg))
            self.queue.task_done()

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

        if len(collisions) > 0:
            self.sounds['pickup'].play()

    def update_points_label(self):

        if self.points < self.new_points:
            self.points += 10
            self.points_label.text = str(self.points)

    def on_update(self, dt):
        self.add_tweets()
        for b in self.tweets:
            b.on_update(dt)

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

        super(GameScene, self).on_draw(window)

        bg_x = -self.player.x
        bg_y = -self.player.y
        if bg_y < - 240:
            bg_y = -240
        self.background.blit(bg_x, bg_y)
        self.batch.draw()
        self.points_label.draw()
