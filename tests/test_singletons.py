#!/usr/bin/env python

"""
Tests for the singleton scope.py
"""

from snakeguice import inject, Injected
from snakeguice import Injector

import cls_heirarchy as ch


class TestSingletonScope(object):

    class DomainObject(object):

        @inject(logger_a=ch.Logger, logger_b=ch.Logger, logger_c=ch.Logger)
        def set_loggers(self, logger_a=Injected, logger_b=Injected,
                logger_c=Injected):
            self.logger_a = logger_a
            self.logger_b = logger_b
            self.logger_c = logger_c

        @inject(place_a=ch.Place, annotation='hot')
        def set_place_a(self, place_a):
            self.place_a = place_a

        @inject(place_b=ch.Place, annotation='hot')
        def set_place_b(self, place_b):
            self.place_b = place_b

        @inject(place_c=ch.Place, annotation='cold')
        def set_place_c(self, place_c):
            self.place_c = place_c

        @inject(place_d=ch.Place, annotation='cold')
        def set_place_d(self, place_d):
            self.place_d = place_d

        @inject(place_d=ch.Place, annotation='cold')
        def set_place_d(self, place_d):
            self.place_d = place_d

    def assert_obj(self, obj):
        assert obj.logger_a is obj.logger_b
        assert obj.logger_b is obj.logger_c
        assert obj.place_a is obj.place_b
        assert obj.place_c is obj.place_d
        assert obj.place_a is not obj.place_d

    def test_to_instance(self):
        class MyModule:
            def configure(self, binder):
                binder.bind(ch.Logger, to_instance=ch.ConcreteLogger())
                binder.bind(ch.Place, annotated_with='hot',
                        to_instance=ch.Beach())
                binder.bind(ch.Place, annotated_with='cold',
                        to_instance=ch.Glacier())

        obj = Injector(MyModule()).get_instance(self.DomainObject)
        self.assert_obj(obj)

    def test_eager_singleton(self):
        class MyModule:
            def configure(self, binder):
                binder.bind(ch.Logger, to_eager_singleton=ch.ConcreteLogger)
                binder.bind(ch.Place, annotated_with='hot',
                        to_eager_singleton=ch.Beach)
                binder.bind(ch.Place, annotated_with='cold',
                        to_eager_singleton=ch.Glacier)

        obj = Injector(MyModule()).get_instance(self.DomainObject)
        self.assert_obj(obj)

    def test_lazy_singleton(self):
        class MyModule:
            def configure(self, binder):
                binder.bind(ch.Logger, to_lazy_singleton=ch.ConcreteLogger)
                binder.bind(ch.Place, annotated_with='hot',
                        to_lazy_singleton=ch.Beach)
                binder.bind(ch.Place, annotated_with='cold',
                        to_lazy_singleton=ch.Glacier)

        obj = Injector(MyModule()).get_instance(self.DomainObject)
        self.assert_obj(obj)

    def __test_inject_into_eager_singleton(self):
        class MyLogger(object):

            @inject(place=ch.Place, annotation='hot')
            def set_hot_place(self, place):
                self.hot_place = place

            @inject(place=ch.Place, annotation='cold')
            def set_cold_place(self, place):
                self.cold_place = place

        class MyModule:
            def configure(self, binder):
                binder.bind(ch.Logger, to_eager_singleton=MyLogger)
                binder.bind(ch.Place, annotated_with='hot',
                        to_eager_singleton=ch.Beach)
                binder.bind(ch.Place, annotated_with='cold',
                        to_eager_singleton=ch.Glacier)

        obj = Injector(MyModule()).get_instance(self.DomainObject)
        self.assert_obj(obj)
        assert obj.logger_a.hot_place is obj.place_a
        assert obj.logger_a.cold_place is obj.place_c

    def _test_inject_into_lazy_singleton(self):
        class MyLogger(object):
            hot_place = inject(ch.Place, annotation='hot')
            cold_place = inject(ch.Place, annotation='cold')

        class MyModule:
            def configure(self, binder):
                binder.bind(ch.Logger, to_lazy_singleton=MyLogger)
                binder.bind(ch.Place, annotated_with='hot',
                        to_lazy_singleton=ch.Beach)
                binder.bind(ch.Place, annotated_with='cold',
                        to_lazy_singleton=ch.Glacier)

        obj = Injector(MyModule()).get_instance(self.DomainObject)
        self.assert_obj(obj)
        assert obj.logger_a.hot_place is obj.place_a
        assert obj.logger_a.cold_place is obj.place_c
