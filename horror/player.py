import pyglet
from .body import Body


class Player(pyglet.sprite.Sprite):

    DIRECTION_LEFT = 0
    DIRECTION_RIGHT = 1
    DIRECTION_UP = 2
    DIRECTION_DOWN = 3

    HORIZ_DIR = (1 << DIRECTION_LEFT) | (1 << DIRECTION_RIGHT)
    VERT_DIR = (1 << DIRECTION_UP) | (1 << DIRECTION_DOWN)

    STATUS_ALIVE = 0
    STATUS_DEAD = 1


    def __init__(self, start_x, start_y, *args, **kwargs):

        super(Player, self).__init__(*args, **kwargs)

        self.set_position(start_x, start_y)

        self.direction = [0, 0]
        self.key_pressed = 0

        self.speed = 150
        self.status = self.STATUS_ALIVE
        self.body = Body()

    def set_image(self, image):
        self.image = image

    def set_animation(self, animation_name):
        self.image = self.animations[animation_name]

    def on_key_pressed(self, direction_key):

        if self.status != self.STATUS_ALIVE:
            return

        key_mask = 1 << direction_key
        if self.key_pressed & key_mask:
            return

        self.key_pressed |= key_mask

        if direction_key == self.DIRECTION_LEFT:
            self.direction[0] = -1
        elif direction_key == self.DIRECTION_RIGHT:
            self.direction[0] = 1

        if direction_key == self.DIRECTION_UP:
            self.direction[1] = 1
        elif direction_key == self.DIRECTION_DOWN:
            self.direction[1] = -1


    def on_key_released(self, direction_key):

        if self.status != self.STATUS_ALIVE:
            return

        key_released = (1 << direction_key)
        self.key_pressed &= ~key_released

        if key_released & self.HORIZ_DIR:
            if self.key_pressed & self.HORIZ_DIR:
                if direction_key == self.DIRECTION_LEFT:
                    self.direction[0] = 1
                elif direction_key == self.DIRECTION_RIGHT:
                    self.direction[0] = -1
            else:
                self.direction[0] = 0

        elif key_released & self.VERT_DIR:
            if self.key_pressed & self.VERT_DIR:
                if direction_key == self.DIRECTION_UP:
                    self.direction[1] = -1
                elif direction_key == self.DIRECTION_DOWN:
                    self.direction[1] = 1
            else:
                self.direction[1] = 0


    def on_animation_end(self):
        if self.status == self.STATUS_DYING:
            self.status = self.STATUS_DEAD

    def die(self):
        self.status = self.STATUS_DEAD
        self.direction[0] = 0
        self.direction[1] = 0

    def is_alive(self):
        return self.status == self.STATUS_ALIVE

    def on_update(self, dt):

        if self.status == self.STATUS_DEAD:
            return False

        self.x += self.speed * self.direction[0] * dt
        self.y += self.speed * self.direction[1] * dt

        if self.x < 0:
            self.x = 0

        if self.x > 640 - self.width:
            self.x = 640 - self.width

        return True

    def bounding_box(self):

        return (self.x, self.y, self.x + self.width, self.y + self.height)
