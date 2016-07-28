from yaff.conf import settings
from yaff.utils.module_loading import import_string


_MATERIALIZED_LOADERS = {}


def get_loader(name):
    """
    returns a callable associated with the specified animation loader
    loaders can be setup by ANIMATION_LOADERS key in the settings file
    default loaders are gif_loader and grid_loader
    :param str name: name of the loader
    """
    try:
        return _MATERIALIZED_LOADERS[name]
    except KeyError:
        _, func = import_string(settings.ANIMATION_LOADERS[name])
        _MATERIALIZED_LOADERS[name] = func
        return func


def load_animation(animation_data):
    func = get_loader(animation_data['loader'])

    params = animation_data['loader_params']
    if isinstance(params, dict):
        return func(**params)
    elif isinstance(params, list):
        return func(*params)
    else:
        return func()
