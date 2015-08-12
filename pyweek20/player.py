import pyglet


class Player(pyglet.sprite.Sprite):

    DIRECTION_LEFT = 0
    DIRECTION_RIGHT = 1

    def __init__(self, start_x, start_y, animations, *args, **kwargs):

        super(Player, self).__init__(*args, **kwargs)

        self.animations = animations
        self.set_position(start_x, start_y)

        self.direction = [0, 0]
        self.key_pressed = 0

        self.speed = 100

    def set_image(self, image):
        self.image = image

    def set_key_pressed(self, direction_key):

        key_mask = 1 << direction_key
        if self.key_pressed & key_mask:
            return

        if direction_key == self.DIRECTION_LEFT:
            self.direction[0] = -1
            self.set_image(self.animations['walk'])
        elif direction_key == self.DIRECTION_RIGHT:
            self.direction[0] = 1
            self.set_image(self.animations['walk'])

        self.key_pressed |= key_mask

    def set_key_released(self, direction_key):

        self.key_pressed &= ~(1 << direction_key)

        if self.key_pressed != 0:
            if direction_key == self.DIRECTION_LEFT:
                self.set_key_pressed(self.DIRECTION_RIGHT)
            elif direction_key == self.DIRECTION_RIGHT:
                self.set_key_pressed(self.DIRECTION_LEFT)
        else:
            self.set_image(self.animations['idle'])
            self.direction[0] = 0

    def set_direction(self, dir_x, dir_y):
        self.direction[0] = dir_x
        self.direction[1] = dir_y

    def on_update(self, dt):

        self.x += self.speed * self.direction[0] * dt
        self.y += self.speed * self.direction[1] * dt

        return True
