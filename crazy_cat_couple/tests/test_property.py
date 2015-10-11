from lib.property import DynamicProperty

def test_property_decay():

    p = DynamicProperty(name='test',
                        initial_value=1,
                        min_value=0,
                        max_value=2,
                        decay_by_sec=1,
                        gain_by_sec=1)

    assert p.decay(1) == 0

def test_property_gain():

    p = DynamicProperty(name='test',
                        initial_value=1,
                        min_value=0,
                        max_value=2,
                        decay_by_sec=1,
                        gain_by_sec=1)

    assert p.gain(1) == 2

def test_property_reset():

    p = DynamicProperty(name='test',
                        initial_value=1,
                        min_value=0,
                        max_value=2,
                        decay_by_sec=1,
                        gain_by_sec=1)

    p.decay(0.2)
    assert p.reset() == 1
