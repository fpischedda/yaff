"""
Mixin class that updates the object direction applying fake gravity
"""


class GravityMixin:

    def __init__(self, gravity, *args, **kwargs):
        self.gravity = gravity
        super(GravityMixin, self).__init__(*args, **kwargs)

    def new_direction(self, dt):
        return (self.direction[0],
                self.direction[1] - self.gravity * dt)

    def on_update(self, dt):
        self.direction = self.new_direction(dt)
        super(GravityMixin, self).on_update(dt)
