import random
import math
import pyglet
import queue
import threading
import settings
from yaff.scene import Scene
from ball import Ball
from letter import Letter
from bitmap_font import BitmapFont
from consumer import Consumer


def feeds_worker(message_queue):

    consumer = Consumer(settings.BROKER_URL, message_queue)

    try:
        consumer.start_consuming()
    except:
        consumer.close_connection()


def randomize_ball(boundaries, image, batch, msg):
    angle = random.randint(0, 360) * 3.14 / 360
    direction = [math.cos(angle), math.sin(angle)]
    b = Ball(msg, boundaries, direction, image, batch=batch)
    b.x = random.randint(30, 600)
    b.y = random.randint(30, 400)

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
        l = Letter(3.0, boundaries,
                    direction,
                    letter_image,
                    batch=batch)
        l.x = start_x
        l.y = start_y

        letters.append(l)
        angle += angle_diff

    return letters


class GameScene(Scene):

    def __init__(self, *args, **kwargs):

        super(GameScene, self).__init__(*args, **kwargs)

        self.image = pyglet.resource.image('res/images/sprites/sprite.png')

        self.queue = queue.Queue()

        self.boundaries = [0, 0, 640, 480]

        self.bitmap_font = BitmapFont('res/images/fonts/font.png', 5, 10)
        self.batch = pyglet.graphics.Batch()
        self.balls = []
        self.letters = []

        self.background = pyglet.resource.image('res/images/bg/bg.jpg')

        self.start_feeds_thread()

    def start_feeds_thread(self):

        print("starting feed thread...")
        t = threading.Thread(target=feeds_worker, args=(self.queue,))
        t.daemon = True
        t.start()

        print("feed thread started...")
        self.thread = t

    def on_key_press(self, symbol, modifier):
        if symbol == pyglet.window.key.M:
            self.boundaries[0] += 10
            self.boundaries[1] += 10
            self.boundaries[2] -= 10
            self.boundaries[3] -= 10

        if symbol == pyglet.window.key.N:
            self.boundaries[0] -= 10
            self.boundaries[1] -= 10
            self.boundaries[2] += 10
            self.boundaries[3] += 10

        if symbol == pyglet.window.key.SPACE:
            b = self.balls.pop(0)
            new_letters = spawn_letters(self.bitmap_font, b.die(),
                                        b.x, b.y, self.batch,
                                        self.boundaries)
            self.letters.extend(new_letters)

        return True

    def add_balls(self):

        while not self.queue.empty():
            msg = self.queue.get()
            self.balls.append(randomize_ball(self.boundaries,
                                             self.image,
                                             self.batch,
                                             msg))
            self.queue.task_done()

    def on_update(self, dt):
        self.add_balls()
        for b in self.balls:
            b.on_update(dt)

        to_remove = [l for l in self.letters if l.on_update(dt) is False]
        for r in to_remove:
            self.letters.remove(r)

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)

        self.background.blit(0, 0)
        self.batch.draw()
