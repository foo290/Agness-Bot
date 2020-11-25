from .custom_exceptions import ConfigSettingNotFound


class Config(dict):
    def __init__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, item):
        found = self.get(item)
        if found is None:
            raise ConfigSettingNotFound
        return found

