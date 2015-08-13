import pyglet
import settings


class Player(pyglet.sprite.Sprite):

    DIRECTION_LEFT = 0
    DIRECTION_RIGHT = 1
    DIRECTION_UP = 2

    def __init__(self, start_x, start_y, animations, *args, **kwargs):

        super(Player, self).__init__(*args, **kwargs)

        self.animations = animations
        self.set_position(start_x, start_y)

        self.direction = [0, 0]
        self.key_pressed = 0

        self.speed = 150
        self.jumping = False

    def set_image(self, image):
        self.image = image

    def set_animation(self, animation_name):
        self.image = self.animations[animation_name]

    def set_key_pressed(self, direction_key):

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
            self.direction[1] = 15
            if self.direction[0] < 0:
                self.set_animation('rolling-left')
            else:
                self.set_animation('rolling-right')

    def set_key_released(self, direction_key):

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

    def on_update(self, dt):

        self.x += self.speed * self.direction[0] * dt
        self.y += self.speed * self.direction[1] * dt

        if self.jumping:
            self.direction[1] -= settings.GRAVITY / 4 * dt

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
