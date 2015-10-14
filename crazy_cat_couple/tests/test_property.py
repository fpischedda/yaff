import pytest
from lib.property import DynamicProperty


@pytest.fixture
def property():
    return DynamicProperty(name='test',
                           initial_value=1,
                           min_value=0,
                           max_value=2,
                           decay_by_sec=1,
                           gain_by_sec=1)


def test_property_decay(property):
    assert property.decay(1) == 0


def test_property_gain(property):
    assert property.gain(1) == 2


def test_property_reset(property):
    property.decay(0.2)
    assert property.reset() == 1


def test_to_minimum(property):
    assert property.to_minimum() == 0


def test_to_maximum(property):
    assert property.to_maximum() == 2


def test_lt(property):
    assert property < 5


def test_le(property):
    assert property <= 1


def test_gt(property):
    assert property > 0


def test_ge(property):
    assert property >= 1


def test_eq(property):
    assert property == 1


def test_ne(property):
    assert property != 5
