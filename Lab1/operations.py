from enum import Enum


class Operation(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3

    @staticmethod
    def from_str(s: str):
        s = s.strip()
        s = s.upper()

        match s:
            case "ADD":
                return Operation.ADD
            case "SUB":
                return Operation.SUB
            case "MUL":
                return Operation.MUL
            case "DIV":
                return Operation.DIV
            case _:
                raise ValueError


def do_operation(x: float, y: float, opr: Operation):
    match opr:
        case Operation.ADD:
            return x + y
        case Operation.SUB:
            return x - y
        case Operation.MUL:
            return x * y
        case Operation.DIV:
            if y == 0:
                raise ZeroDivisionError
            return x / y
        case _:
            raise NotImplementedError
