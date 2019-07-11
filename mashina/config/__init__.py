import os
import importlib


class LazySettings(object):

    def __init__(self):
        self._wrapped = None

    def __getattr__(self, attr):
        if self._wrapped is None:
            self._wrapped = Settings()
        return getattr(self._wrapped, attr)


class Settings(object):
    def __init__(self):
        mod = importlib.import_module(os.getenv('MASHINA_SETTINGS_MODULE'))
        for setting in dir(mod):
            if setting.isupper():
                setattr(self, setting, getattr(mod, setting))


settings = LazySettings()
