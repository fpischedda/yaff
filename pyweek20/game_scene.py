import random
import math
import pyglet
import queue
import threading
import settings
from yaff.scene import Scene
from tweet import Tweet
from letter import Letter
from player import Player
from bitmap_font import BitmapFont
from consumer import Consumer


def feeds_worker(message_queue):

    consumer = Consumer(settings.BROKER_URL, message_queue)

    try:
        consumer.start_consuming()
    except:
        consumer.close_connection()


def degrees_to_radians(degrees):
    return degrees * 3.14 / 360

def randomize_starting_point():
    if random.random() >= 0.5:
        return (degrees_to_radians(random.randint(40, 70)), 40, 0)

    return (degrees_to_radians(random.randint(120, 150)), 600, 0)


def randomize_tweet(image, batch, msg):

    angle, x, y = randomize_starting_point()

    direction = [math.cos(angle), math.sin(angle)]
    b = Tweet(msg, direction, image, batch=batch)
    b.x = x
    b.y = y

    return b


def spawn_letters(bitmap_font, text, start_x, start_y, batch, boundaries):

    points = len(text)
    if points <= 0:
        return []

    letters = []
    angle = 0
    angle_diff = 360 / points
    for letter in text:
        letter_image = bitmap_font.get_image(letter)
        direction = [math.cos(angle), math.sin(angle)]
        l = Letter(5.0, boundaries,
                   direction,
                   letter_image,
                   batch=batch)
        l.x = start_x
        l.y = start_y

        letters.append(l)
        angle += angle_diff

    return letters


def load_animation(path, tex_bin=None):

    tb = tex_bin or pyglet.image.atlas.TextureBin()
    animation = pyglet.image.load_animation(path)
    animation.add_to_texture_bin(tb)

    return animation


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

        tex_bin = pyglet.image.atlas.TextureBin()
        player_animations = {
            'idle': load_animation('res/images/sprites/cat_idle.gif', tex_bin),
            'walk': load_animation('res/images/sprites/cat_walk.gif', tex_bin),
            'die': load_animation('res/images/sprites/cat_die.gif', tex_bin),
        }

        self.player = Player(320, 0, player_animations,
                             player_animations['idle'],
                             batch=self.batch)

        self.background = pyglet.resource.image('res/images/bg/bg.jpg')

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

    def on_key_press(self, symbol, modifier):

        if symbol == pyglet.window.key.A:
            self.player.set_key_pressed(Player.DIRECTION_LEFT)
        elif symbol == pyglet.window.key.D:
            self.player.set_key_pressed(Player.DIRECTION_RIGHT)

        if symbol == pyglet.window.key.SPACE:
            b = self.tweets.pop(0)
            new_letters = spawn_letters(self.bitmap_font, b.die(),
                                        b.x, b.y, self.batch,
                                        self.boundaries)
            self.letters.extend(new_letters)

        return True

    def add_tweets(self):

        while not self.queue.empty():
            msg = self.queue.get()
            self.tweets.append(randomize_tweet(self.image,
                                             self.batch,
                                             msg))
            self.queue.task_done()

    def on_update(self, dt):
        self.add_tweets()
        for b in self.tweets:
            b.on_update(dt)

        to_remove = [l for l in self.letters if l.on_update(dt) is False]
        for r in to_remove:
            self.letters.remove(r)

        self.player.on_update(dt)

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)

        self.background.blit(0, 0)
        self.batch.draw()
