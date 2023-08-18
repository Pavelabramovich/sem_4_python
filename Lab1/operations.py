import operator
from enum import Enum


# __call__ overrided for normal work of enum fields as functions.
class Operation(Enum):
    ADD = operator.add
    SUB = operator.sub
    MUL = operator.mul
    DIV = operator.truediv

    def __call__(self, *args):
        return self.value(*args)
