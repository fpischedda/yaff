class SettingNotFound(Exception):
    pass


class BaseSettings(object):

    def __getattr__(self, attr):

        try:
            return self._settings[attr]
        except KeyError:
            raise SettingNotFound("setting %s not found" % attr)

settings = BaseSettings()
