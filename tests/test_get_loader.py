from yaff.animation.loaders import gif_loader
from yaff.animation import get_loader


def test_get_loader():
    """
    tests if get_loader returns the correct function as defined in
    conf.settings
    """

    func = get_loader('gif')
    assert func == gif_loader
