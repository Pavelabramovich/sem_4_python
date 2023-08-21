import unittest
from unittest import TestCase
from SerializationOfClassesAndFuncs import SerializersFactory, SerializerType

from tests.objects_for_test import (
    PRIMITIVES,
    rec_func,
    gen_func,
    decorated_func,
    A, B
)


class SerializationTestCase(TestCase):

    def setUp(self):
        self.json = SerializersFactory.create_serializer(SerializerType.JSON)

    def test_primitives(self):
        """Test primitive types json serialization"""

        primitives = self.json.dumps(PRIMITIVES)
        primitives = self.json.loads(primitives)

        self.assertEqual(PRIMITIVES, primitives)

    def test_nested_list(self):
        l = [1, 2, 3]
        l[0] = l

        L = [1,2,3, l]

        sL = self.json.dumps(L)
        sL = self.json.loads(sL)

        with self.assertRaises(RecursionError):
            self.assertSequenceEqual(L, sL)

    def test_filter(self):
        l = [1, 2, 3, 4, 5, 6]
        f1 = filter(lambda n: n % 2 == 0, l)
        f2 = filter(lambda n: n % 2 == 0, l)

        sf = self.json.dumps(f1)
        sf = self.json.loads(sf)

        self.assertSequenceEqual(list(f2), list(sf))

    def test_inf(self):
        t = (10E1000, -10E1000, 10E1000 / 10E1000)

        print(t)

        st = self.json.dumps(t)
        st = self.json.loads(st)

        self.assertSequenceEqual(str(t), str(st))

    def test_ellipsis(self):

        e = self.json.dumps(...)
        e = self.json.loads(e)

        self.assertEqual(e, ...)

    def test_not_implemented(self):

        sni = self.json.dumps(NotImplemented)
        sni = self.json.loads(sni)

        self.assertEqual(sni, NotImplemented)

    def test_uion(self):
        u = int | dict | bool | str

        su = self.json.dumps(u)
        su = self.json.loads(su)

        self.assertEqual(su, u)

    def test_generic_alias(self):
        g = list[int | str, str]

        sg = self.json.dumps(g)
        sg = self.json.loads(sg)

        self.assertEqual(sg, g)

    def test_dict_items(self):
        d = {1: 1, 2: 2}
        items = d.keys()

        s_items = self.json.dumps(items)
        s_items = self.json.loads(s_items)

        self.assertSequenceEqual(tuple(items), s_items)

    def test_nested_class(self):
        class C:
            def __init__(self):
                self.c = C

            def prnt(self):
                a = C
                print(a().c)

        C.d = C




        sC = self.json.dumps(C)
        sC = self.json.loads(sC)

        sC().prnt()

    def test_not_object_base(self):
        class TestDict(dict):
            def add_item(self, key, value):
                super().update({key: value})

        d = TestDict()

        # with open("data_file.json", "w") as file:
        #     self.json.dump(d, file)

        sd = self.json.dumps(d)
        sd = self.json.loads(sd)

        d.add_item(2, "234")
        sd.add_item(2, "234")

        print(d.items())
        print(type(sd.items()))

        self.assertSequenceEqual(d.items(), sd.items())

    def test_func(self):
        """Test func json serialization"""

        func = self.json.dumps(rec_func)
        func = self.json.loads(func)

        before = [rec_func(i) for i in range(100)]
        after = [func(i) for i in range(100)]

        self.assertEqual(before, after)

    def test_gen_func(self):
        """Test gen func serialization"""

        s_gen = self.json.dumps(gen_func)
        s_gen = self.json.loads(s_gen)

        before = [*gen_func()]
        after = [*s_gen()]

        self.assertEqual(before, after)

    def test_gen(self):
        """Test gen serialization"""

        gen1 = gen_func()
        gen2 = gen_func()

        s_gen = self.json.dumps(gen1)
        s_gen = self.json.loads(s_gen)

        before = [*gen2]
        after = [*s_gen]

        self.assertEqual(before, after)

    def test_decorator(self):
        """Test decorator serialization"""

        df = self.json.dumps(decorated_func)
        df = self.json.loads(df)

        before = [decorated_func(i) for i in range(100)]
        after = [df(i) for i in range(100)]

        self.assertEqual(before, after)



    def test_class(self):
        """Test class serialization"""

        with open("data_file.json", "w") as file:
            self.json.dump(B, file)

        sB = self.json.dumps(B)
        sB = self.json.loads(sB)

        q = sB("name")
        q.name = "123"

        before = [B.a, B.b, B.c, B._X, B.bx_test(), B.sttmet(), B("name").name]
        after = [sB.a, sB.b, sB.c, sB._X, sB.bx_test(), sB.sttmet(), sB("name").name]

        self.assertEqual(before, after)

    def test_object(self):
        """Test object serialization"""



        b = B("123")

        # with open("data_file.json", "w") as file:
        #     self.json.dump(b, file)

        sb = self.json.dumps(b)
        sb = self.json.loads(sb)

        b.name = "qwe"
        sb.name = "qwe"

        b.inf()
        sb.inf()

        self.assertEqual(b.name, sb.name)


if __name__ == '__main__':
    unittest.main()
