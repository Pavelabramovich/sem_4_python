from serializers_factory import SerializersFactory, SerializerType


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
    a = "A"


class B(A):
    a = "B"


class C(A):
    a = "C"


class D(B, C):
    a = "D"


if __name__ == '__main__':

    o = None
    #o = 103
    #o = {1:{1:{1:{1:{1:{1:{1:1}}}}}}}

    s = SerializersFactory.create_serializer(SerializerType.XML)

    with open("data_file.xml", "w") as file:
        s.dump(T.tst4, file)
    with open("data_file.xml", "r") as file:
        a = s.load(file)

    print(a)

    print(T.__dict__)
    print(a.__dict__)

    print(a)
    print(a._X)
    print(a.A)
    print(a.tst4())
    print(a.clsmet())
    print(a.lol())
    print(a._LOL)

    # x = JsonSerializer.dumps(T.clsmet)
    # print(x)
    # y = JsonSerializer.loads(x)



