
class BaseProperty:

    def __init__(self, name, value, *args, **kwargs):
        super(BaseProperty, self).__init__(*args, **kwargs)

        self.value = value
        self.name = name


class DecayingPropertyMixin:

    DECAYING_ATTIBUTE = 'value'

    def __init__(self, decay_by_sec, min_value, *args, **kwargs):

        super(DecayingPropertyMixin, self).__init__(*args, **kwargs)

        self.decay_by_sec = decay_by_sec
        self.min_value = min_value

    def to_minimum(self):
        setattr(self, self.DECAYING_ATTIBUTE, self.min_value)
        return getattr(self, self.DECAYING_ATTIBUTE)

    def decay(self, dt):
        val = getattr(self, self.DECAYING_ATTIBUTE)

        new_val = max(val - self.decay_by_sec * dt, self.min_value)

        setattr(self, self.DECAYING_ATTIBUTE, new_val)
        return new_val


class GainingPropertyMixin:

    GAINING_ATTRIBUTE = 'value'

    def __init__(self, gain_by_sec, max_value, *args, **kwargs):

        super(GainingPropertyMixin, self).__init__(*args, **kwargs)

        self.gain_by_sec = gain_by_sec
        self.max_value = max_value

    def to_maximum(self):
        setattr(self, self.DECAYING_ATTIBUTE, self.max_value)
        return getattr(self, self.DECAYING_ATTIBUTE)

    def gain(self, dt):
        val = getattr(self, self.GAINING_ATTRIBUTE)
        
        new_val = min(val + self.decay_by_sec * dt, self.max_value)

        setattr(self, self.GAINING_ATTRIBUTE, new_val)
        return new_val
        
class DynamicProperty(BaseProperty, DecayingPropertyMixin, GainingPropertyMixin):

    def __init__(self, initial_value, *args, **kwargs):
        if 'value' not in kwargs:
            kwargs['value'] = initial_value
        super(DynamicProperty, self).__init__(*args, **kwargs)

        self.initial_value = initial_value

    def reset(self):
        self.value = self.initial_value
        return self.value
