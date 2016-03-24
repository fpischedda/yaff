from yaff.utils.module_loading import import_string
import yaff.animation.loaders


def test_import_string():
    """tests if import_string loads the correct module and attribute/class"""

    module, func = import_string('yaff.animation.loaders.gif_loader')
    assert module == yaff.animation.loaders
    assert func == yaff.animation.loaders.gif_loader
