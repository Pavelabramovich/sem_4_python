import unittest
from datetime import date, time, datetime, timedelta
from unittest import TestCase
from SerializationOfClassesAndFuncs import JsonSerializer

from tests.objects_for_test import (
    PRIMITIVES,
    rec_func,
    gen_func,
    decorated_func,
    B
)


class SerializationTestCase(TestCase):
    def setUp(self):
        self.json = JsonSerializer()

    def test_primitives(self):
        primitives = self.json.dumps(PRIMITIVES)
        primitives = self.json.loads(primitives)

        self.assertEqual(PRIMITIVES, primitives)

    def test_nested_list(self):
        l = [1, 2, 3]
        l[0] = l

        L = [1, 2, 3, l]

        sL = self.json.dumps(L)
        sL = self.json.loads(sL)

        with self.assertRaises(RecursionError):
            self.assertSequenceEqual(L, sL)

    def test_inf_nan(self):
        t = (10E1000, -10E1000, 10E1000 / 10E1000)

        st = self.json.dumps(t)
        st = self.json.loads(st)

        # str because nan != nan
        self.assertSequenceEqual(str(t), str(st))

    def test_datetime(self):
        d = date(year=1, month=2, day=3)
        t = time(hour=10, minute=20, second=30, microsecond=40)
        dt = datetime.combine(date=d, time=t)
        td = timedelta(weeks=10, days=3, hours=10, minutes=10, seconds=2, milliseconds=2, microseconds=45)

        l = [d, t, dt, td]

        sl = self.json.dumps(l)
        sl = self.json.loads(sl)

        self.assertSequenceEqual(l, sl)

    def test_ellipsis(self):
        e = self.json.dumps(...)
        e = self.json.loads(e)

        self.assertEqual(e, ...)

    def test_not_implemented(self):
        sni = self.json.dumps(NotImplemented)
        sni = self.json.loads(sni)

        self.assertEqual(sni, NotImplemented)

    def test_union(self):
        u = int | dict | bool | str

        su = self.json.dumps(u)
        su = self.json.loads(su)

        self.assertEqual(su, u)

    def test_generic_alias(self):
        g = dict[int | str, str]

        sg = self.json.dumps(g)
        sg = self.json.loads(sg)

        self.assertEqual(sg, g)

    def test_filter(self):
        l = [1, 2, 3, 4, 5, 6]
        f1 = filter(lambda n: n % 2 == 0, l)
        f2 = filter(lambda n: n % 2 == 0, l)

        sf = self.json.dumps(f1)
        sf = self.json.loads(sf)

        self.assertSequenceEqual(list(f2), list(sf))

    def test_dict_items(self):
        d = {1: 1, 2: 2}
        items = d.keys()

        s_items = self.json.dumps(items)
        s_items = self.json.loads(s_items)

        self.assertSequenceEqual(tuple(items), s_items)

    def test_builtin(self):
        a = abs

        sa = self.json.dumps(a)
        sa = self.json.loads(sa)

        self.assertEqual(sa(-2), 2)

    def test_nested_class(self):
        class C:
            def __init__(self):
                self.c = C

            def a(self):
                a = C
                return a().c

            @staticmethod
            def value():
                return "val"

        C.d = C

        sC = self.json.dumps(C)
        sC = self.json.loads(sC)

        self.assertSequenceEqual([C().a().value(), C.d().value()], [sC().a().value(), sC.d().value()])

    def test_func(self):
        func = self.json.dumps(rec_func)
        func = self.json.loads(func)

        before = [rec_func(i) for i in range(100)]
        after = [func(i) for i in range(100)]

        self.assertEqual(before, after)

    def test_gen_func(self):
        s_gen = self.json.dumps(gen_func)
        s_gen = self.json.loads(s_gen)

        before = [*gen_func()]
        after = [*s_gen()]

        self.assertEqual(before, after)

    def test_gen(self):
        gen1 = gen_func()
        gen2 = gen_func()

        s_gen = self.json.dumps(gen1)
        s_gen = self.json.loads(s_gen)

        before = [*gen2]
        after = [*s_gen]

        self.assertEqual(before, after)

    def test_decorator(self):
        df = self.json.dumps(decorated_func)
        df = self.json.loads(df)

        before = [decorated_func(i) for i in range(100)]
        after = [df(i) for i in range(100)]

        self.assertEqual(before, after)

    def test_class(self):
        sB = self.json.dumps(B)
        sB = self.json.loads(sB)

        before = [B.a, B.b, B.c, B._X, B.bx_test(), B.sttmet(), B("name").name]
        after = [sB.a, sB.b, sB.c, sB._X, sB.bx_test(), sB.sttmet(), sB("name").name]

        self.assertEqual(before, after)

    def test_object(self):
        b = B("123")

        sb = self.json.dumps(b)
        sb = self.json.loads(sb)

        b.name = "qwe"
        sb.name = "qwe"

        self.assertSequenceEqual([b.name, b.inf()], [sb.name, sb.inf()])

    def test_singleton(self):
        second_serializer = JsonSerializer()

        self.assertEqual(self.json, second_serializer)


if __name__ == '__main__':
    unittest.main()
