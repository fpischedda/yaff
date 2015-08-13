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
        self.background = pyglet.resource.image('res/images/bg/bg.jpg')

        self.explosion_animation = load_grid_animation(
            'res/images/sprites/explosion.png', 1, 6
        )

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

        if symbol == pyglet.window.key.SPACE:
            b = self.tweets.pop(0)

        return True

    def add_tweets(self):

        while not self.queue.empty():
            msg = self.queue.get()
            self.tweets.append(randomize_tweet(self.bird_animations,
                                               self.batch,
                                               msg))
            self.queue.task_done()

    def check_collisions(self):
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

    def on_update(self, dt):
        self.add_tweets()
        for b in self.tweets:
            b.on_update(dt)

        self.check_collisions()

        to_remove = [l for l in self.letters if l.on_update(dt) is False]
        for r in to_remove:
            self.letters.remove(r)

        self.player.on_update(dt)

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)

        self.background.blit(0, 0)
        self.batch.draw()
