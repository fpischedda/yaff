from ..property import DynamicProperty

def test_property_decay():

    p = DynamicProperty(name='test',
                        initial_value=1,
                        min_value=0,
                        max_value=2,
                        decai_per_sec=1,
                        gain_per_sec=1)

    assert p.decay(1) == 0
