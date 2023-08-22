PRIMITIVES = [10, 1.34, "string", "[1 , 2, 3, 5]", [1, 2, 3], {1: {1: {1: {1: {1: 1}}}}}, None, True, False,
              1 + 5j, {1, 2, 3, 4}, (1, 4), frozenset({1, 2}), [], bytes([48, 49, 50]), bytearray([51, 52, 53])]


class A:
    def __init__(self, name):
        self._name = name

    @staticmethod
    def sttmet():
        return "var"

    @classmethod
    def clsmet(cls):
        return cls._VAR

    @property
    def name(self):
        return self._name + str(self._VAR)

    @name.setter
    def name(self, value):
        self._name = value

    def f(self):
        return 1

    _VAR = 1 - 0


class B(A):
    _X = 11

    a = 10
    b = 11
    c = 14

    @staticmethod
    def bx_test():
        return 123 * B._X

    def __init__(self, name):
        super().__init__(name)
        self.xy = 10

    def inf(self):
        return f"{self.xy}_and_{self._VAR}"


def rec_func(a):
    return rec_func(a - 1) + 1 if a > 1 else 1


def my_decorator(func):
    def cwrapper(*args, **kwargs):
        return 10 * func(*args, **kwargs)

    return cwrapper


def for_dec(a):
    return 2 * a


decorated_func = my_decorator(for_dec)


def gen_func():
    for i in range(10):
        yield i
