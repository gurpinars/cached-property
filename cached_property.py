class cached_property(object):
    def __init__(self, function):
        self.func = function
        self.args = None
        self._cached = {}

    def __get__(self, obj, klass=None):
        def wrapper(obj):
            def _wrapper(*args, **kwargs):
                self.args = args
                if self.key not in self._cached:
                    print("cached!")
                    self._cached.update(
                        {self.key: self.func(obj, *args, **kwargs)}
                    )
                return self._cached.get(self.key)
            return _wrapper
        return wrapper(obj)

    def _key(self, *args):
        return self.func.__name__, args

    @property
    def key(self):
        return self._key(*self.args)
