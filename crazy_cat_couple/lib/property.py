from collections import namedtuple

BaseDynamicProperty = namedtuple('BaseDynamicProperty',
                                 ['name', 'value', 'initial_value',
                                  'min_value', 'max_value',
                                  'decay_by_sec', 'gain_by_sec'])


class DynamicProperty(BaseDynamicProperty):

    def __init__(self, *args, **kwargs):
        super(DynamicProperty, self).__init__(*args, **kwargs)
        self.value = self.initial_value

    def reset(self):
        self.value = self.initial_value

    def decay(self, dt):
        new_val = self.value - self.decay_by_sec * dt

        self.value = max(new_val, self.min_value)
        return self.value

    def gain(self, dt):
        new_val = self.value + self.decay_by_sec * dt

        self.value = min(new_val, self.max_value)
        return self.value
