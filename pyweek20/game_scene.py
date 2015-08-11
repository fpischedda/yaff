import random
import math
import pyglet
import queue
import threading
import settings
from yaff.scene import Scene
from ball import Ball
from consumer import Consumer


def feeds_worker(message_queue):

    consumer = Consumer(settings.BROKER_URL, message_queue)

    try:
        consumer.start_consuming()
    except:
        consumer.close_connection()


def randomize_ball(boundaries, image, batch, scale):
    angle = random.randint(0, 360) * 3.14 / 360
    direction = [math.cos(angle), math.sin(angle)]
    b = Ball(boundaries, direction, image, batch=batch)
    b.x = random.randint(30, 600)
    b.y = random.randint(30, 400)
    b.scale = scale

    return b


class GameScene(Scene):

    def __init__(self, *args, **kwargs):

        super(GameScene, self).__init__(*args, **kwargs)

        self.image = pyglet.resource.image('res/images/sprites/sprite.png')

        self.queue = queue.Queue()

        self.boundaries = [0, 0, 640, 480]

        self.batch = pyglet.graphics.Batch()
        self.balls = []

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

        return True

    def add_balls(self):

        while not self.queue.empty():
            msg = self.queue.get()
            print(msg)
            scale = len(msg['text']) / 140.0
            self.balls.append(randomize_ball(self.boundaries,
                                             self.image,
                                             self.batch,
                                             scale))
            self.queue.task_done()

    def on_update(self, dt):
        self.add_balls()
        for b in self.balls:
            b.on_update(dt)

    def on_draw(self, window):

        super(GameScene, self).on_draw(window)

        self.background.blit(0, 0)
        self.batch.draw()
