import unittest
from cached_property import cached_property


class TestCachedProperty(unittest.TestCase):
    def test_method(self):
        def factory():
            class Foo(object):
                @cached_property
                def foo(self, num):
                    return num * 2
            return Foo

        obj = factory()
        res = obj.foo(2)
        for cell in obj.foo.__closure__:
            if cell.cell_contents is not None:
                for expected in cell.cell_contents.cache.values():
                    self.assertEqual(expected, res)