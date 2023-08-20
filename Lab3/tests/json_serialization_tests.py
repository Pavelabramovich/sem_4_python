import unittest
from unittest import TestCase
from SerializationOfClassesAndFuncs import SerializersFactory, SerializerType

from tests.objects_for_test import (
    PRIMITIVES,
    rec_func,
    gen,
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

    def test_func(self):
        """Test func json serialization"""

        func = self.json.dumps(rec_func)
        func = self.json.loads(func)

        before = [rec_func(i) for i in range(100)]
        after = [func(i) for i in range(100)]

        self.assertEqual(before, after)

    def test_gen(self):
        """Test gen serialization"""

        s_gen = self.json.dumps(gen)
        s_gen = self.json.loads(s_gen)

        before = [*gen()]
        after = [*s_gen()]

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


if __name__ == '__main__':
    unittest.main()
