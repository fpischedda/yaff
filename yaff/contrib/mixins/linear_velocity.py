import math


class LinearVelocityMixin(object):
    """"
    simple mixin to add linear velocity to a sprite
    this mixin will intercept on_update call to update sprite position
    accordingly with its velocity and elapsed delta time since last frame
    """

    LINEAR_VELOCITY_MIXIN_X_ATTRIBUTE = 'x'
    LINEAR_VELOCITY_MIXIN_Y_ATTRIBUTE = 'y'

    def __init__(self, direction, speed, *args, **kwargs):

        self.direction = direction
        self.speed = speed
        self.__init__(LinearVelocityMixin, *args, **kwargs)

    def set_speed(self, speed):
        self.speed = speed

    def set_direction(self, x_dir, y_dir):
        self.direction = (x_dir, y_dir)

    def ser_direction_from_angle(self, angle):
        self.direction = (math.cos(angle), math.sin(angle))

    def on_update(self, dt):
        super(LinearVelocityMixin, self).on_update(dt)

        scaled_speed = self.speed * dt
        x = getattr(self, self.LINEAR_VELOCITY_MIXIN_X_ATTRIBUTE)
        y = getattr(self, self.LINEAR_VELOCITY_MIXIN_Y_ATTRIBUTE)

        setattr(self, self.LINEAR_VELOCITY_MIXIN_X_ATTRIBUTE,
                x + self.direction[0] * scaled_speed)
        setattr(self, self.LINEAR_VELOCITY_MIXIN_Y_ATTRIBUTE,
                y + self.direction[1] * scaled_speed)
