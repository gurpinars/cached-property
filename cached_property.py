class CachedMeta(type):
    def __new__(cls, name, bases, clsdict):
        clsdict['cache'] = dict()
        clsdict['args'] = None
        clsobj = super(CachedMeta, cls).__new__(cls, name, bases, clsdict)
        return clsobj


class cached_property(metaclass=CachedMeta):
    def __init__(self, function):
        self.func = function

    def __get__(self, obj, klass=None):
        def wrapper(obj):
            def _wrapper(*args, **kwargs):
                self.args = args
                if self.key not in self.cache:
                    self.cache.update(
                        {self.key: self.func(obj, *args, **kwargs)}
                    )
                return self.cache.get(self.key)
            return _wrapper
        return wrapper(obj)

    def _key(self, *args):
        return self.func.__name__, args

    @property
    def key(self):
        return self._key(*self.args)
