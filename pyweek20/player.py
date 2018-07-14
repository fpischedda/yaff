import pyglet
from . import settings


class Player(pyglet.sprite.Sprite):

    DIRECTION_LEFT = 0
    DIRECTION_RIGHT = 1
    DIRECTION_UP = 2

    STATUS_ALIVE = 0
    STATUS_DYING = 1
    STATUS_DEAD = 2

    def __init__(self, start_x, start_y, animations, *args, **kwargs):

        super(Player, self).__init__(*args, **kwargs)

        self.animations = animations
        self.set_position(start_x, start_y)

        self.direction = [0, 0]
        self.key_pressed = 0

        self.speed = 150
        self.jumping = False

        self.status = self.STATUS_ALIVE
        self.sounds = {
            'jump': pyglet.resource.media('sfx/player_jump.wav',
                                          streaming=False),
            'die': pyglet.resource.media('sfx/player_died.wav',
                                         streaming=False),
        }

    def set_image(self, image):
        self.image = image

    def set_animation(self, animation_name):
        self.image = self.animations[animation_name]

    def set_key_pressed(self, direction_key):

        if self.status != self.STATUS_ALIVE:
            return

        key_mask = 1 << direction_key
        if self.key_pressed & key_mask:
            return

        self.key_pressed |= key_mask

        if direction_key == self.DIRECTION_LEFT:
            self.direction[0] = -1

            if self.jumping:
                self.set_animation('rolling-left')
            else:
                self.set_animation('run-left')

        elif direction_key == self.DIRECTION_RIGHT:
            self.direction[0] = 1
            if self.jumping:
                self.set_animation('rolling-right')
            else:
                self.set_animation('run-right')

        if direction_key == self.DIRECTION_UP and not self.jumping:
            self.jumping = True
            self.direction[1] = 5
            if self.direction[0] < 0:
                self.set_animation('rolling-left')
            else:
                self.set_animation('rolling-right')

            # self.sounds['jump'].play()

    def set_key_released(self, direction_key):

        if self.status != self.STATUS_ALIVE:
            return

        self.key_pressed &= ~(1 << direction_key)

        if self.key_pressed != 0:
            if direction_key == self.DIRECTION_LEFT:
                self.set_key_pressed(self.DIRECTION_RIGHT)
            elif direction_key == self.DIRECTION_RIGHT:
                self.set_key_pressed(self.DIRECTION_LEFT)
        elif not self.jumping:
            if direction_key == self.DIRECTION_LEFT:
                self.set_animation('idle-left')
            else:
                self.set_animation('idle-right')

            self.direction[0] = 0

    def on_animation_end(self):
        if self.status == self.STATUS_DYING:
            self.status = self.STATUS_DEAD

    def die(self):
        # self.sounds['die'].play()
        self.status = self.STATUS_DYING
        self.direction[0] = 0
        self.direction[1] = 0
        self.jumping = False
        self.set_animation('dying')

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

        if self.jumping:
            self.direction[1] -= settings.GRAVITY * dt

        if self.jumping and self.y <= 0:
            self.y = 0
            self.direction[1] = 0
            self.jumping = False
            if self.direction[0] > 0:
                self.set_animation('run-right')
            elif self.direction[0] < 0:
                self.set_animation('run-left')
            else:
                self.set_animation('idle-left')

        return True

    def bounding_box(self):

        return (self.x, self.y, self.x + self.width, self.y + self.height)
