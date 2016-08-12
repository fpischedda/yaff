"""
yaff.conf module exports settings for the application
the settings module can be specified via a YAFF_SETTINGS_MODULE
env variable and defaults to 'settings'
once loaded, user settings are merged with default settings
and are available to user application via yaff.conf.settings
import path
"""
import importlib
import os
from . import global_settings


class ImproperlyConfiguredError(Exception):
    pass


class SettingNotFound(Exception):
    pass


ENV_SETTINGS_MODULE = 'YAFF_SETTINGS_MODULE'


class BaseSettings(object):

    def __init__(self):
        self._settings = {}

        g = {k: getattr(global_settings, k) for k in dir(global_settings)
             if k.isupper()}

        module = os.environ.get(ENV_SETTINGS_MODULE, None)

        if module is not None:
            try:
                sm = importlib.import_module(module)
            except ImportError:
                raise ImproperlyConfiguredError(
                    "Unable to load {} settings module".format(module))

            custom = {k: getattr(sm, k) for k in dir(sm) if k.isupper()}

            # merge defauls with user's custom settings
            self._settings = g.copy()
            self._settings.update(custom)
        else:
            self._settings = g

    def __getattr__(self, attr):

        try:
            return self._settings[attr]
        except KeyError:
            raise SettingNotFound("setting %s not found" % attr)

settings = BaseSettings()
