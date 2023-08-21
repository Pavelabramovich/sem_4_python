import types
import gc

from SerializationOfClassesAndFuncs.serializers_factory import SerializersFactory, SerializerType
import math

import builtins
import inspect
from types import GeneratorType

# D = dict.__new__(dict)
# print(id(D))
# D.update({1: 1, 2: 2})
# items = D.keys()
# print(items)
# D[3] = 3
# print(items)
#
# print(id(gc.get_referents(items.mapping)[0]))
# items.mapping.update({3:4})
# print(items)
#
# for item in inspect.getmembers(items):
#     print(item)

(int | dict).__args__ = str

print(())
print(type(int | int))

print(type(list[int]))

print((int | float).__args__)
print((list[int | float, str]).__args__)
print((list[int]).__origin__)
print(type(list[int]).__dict__)

i = int
i |= str

l = list

print(type(l[int]))

print(int | float == int | float)

for key, value in inspect.getmembers(builtins):
    if type(value) not in (type, types.BuiltinMethodType):
        print(f"{value}")
    # try:
    #     print(f"{value.__name__ = } {value = } {type(value) = }")
    # except (KeyError, AttributeError):
    #     pass

print(abs.__name__)

def tst2(b=10):
    return b + 1


def tst(a):
    return a + a ** 2


tst3 = lambda x: x ** 2


def gen():
    for i in range(10):
        yield i


def tst5():
    def tst6():
        return 18

    return tst6


class t:
    @staticmethod
    def lol():
        return "lol"

    @classmethod
    def clsmet(cls):
        return cls._LOL

    def f(self):
        return 1

    _LOL = 1 - 0


class T(t):
    _X = 11

    A = 10
    B = 11
    C = 14

    @staticmethod
    def tst4():
        return 123 * T._X

    def __init__(self):
        self.xy = 10

    def inf(self):
        print(self.xy, " ", self._LOL)


def my_decorator(func):
    def cwrapper(*args, **kwargs):
        print("start func")
        func(*args, **kwargs)
        print("end func")

    return cwrapper


def for_dec(a):
    print("Hello world", a)


df = my_decorator(for_dec)


class A:
    x = 15

    def __init__(self):
        self.a = 12
        self.b = 10

    def my_meth(self):
        return self.a * self.b


class B:
    def __str__(self):
        return "AAAAAAAA"

    def __repr__(self):
        return "AAAAAAAA"


class C(A, B):
    pass


if __name__ == '__main__':
    s = SerializersFactory.create_serializer(SerializerType.JSON)

    print(int.__bases__)
    print(object.__bases__)


    class cl:
        def __init__(self, st):
            self.st = st

        def __str__(self):
            return str(self.st)


    st = {1, 2, 3, 4}
    st.update({cl(st)})

    print(st)

    l = [1, 2, 3, 4]
    l[0] = l

    print(l)

    obj_s = s.dumps(l)
    print(obj_s)
    obj_d = s.loads(obj_s)

    print(obj_d)

    # print(obj_d(10))
    # print(df(10))

    # o = None
    # #o = 103
    # #o = {1:{1:{1:{1:{1:{1:{1:1}}}}}}}
    #
    # s = SerializersFactory.create_serializer(SerializerType.XML)
    #
    # with open("data_file.json", "w") as file:
    #     s.dump(T, file)
    # with open("data_file.json", "r") as file:
    #     a = s.load(file)
    #
    # print(a)
    #
    # print(a)
    # print(a._X)
    # print(a.A)
    # print(a.tst4())
    # print(a.clsmet())
    # print(a.lol())
    # print(a._LOL)
    #
    # # x = JsonSerializer.dumps(T.clsmet)
    # # print(x)
    # # y = JsonSerializer.loads(x)
