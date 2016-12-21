import unittest
import trace
from cached_property import cached_property


class TestCachedProperty(unittest.TestCase):
    def setUp(self):
        self.f = __file__.split('tests')[0] + 'cached_property.py'
        self.tracer = trace.Trace(trace=0, count=1)
        self.key = (self.f, 13)

    def test_method_call_for_same_value(self):
        def factory():
            class Foo(object):
                @cached_property
                def foo(self, num):
                    return num * 2
            return Foo

        self.obj = factory()

        for i in range(2):
            self.tracer.runfunc(self.obj.foo, 2)

        r = self.tracer.results()

        self.assertEqual(r.counter.get(self.key), 1)

    def test_method_call_for_different_value(self):
        def factory():
            class Foo(object):
                @cached_property
                def foo(self, num):
                    return num * 2
            return Foo

        self.obj = factory()
        self.tracer.runfunc(self.obj.foo, 2)
        self.tracer.runfunc(self.obj.foo, 3)

        r = self.tracer.results()

        self.assertGreater(r.counter.get(self.key), 1)
