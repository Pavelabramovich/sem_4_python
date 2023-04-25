from enum import Enum


class Command(Enum):
    ADD_USER = "ADD USER"
    ADD = "ADD"
    REMOVE = "REMOVE"

    FIND = "FIND"
    LIST = "LIST"
    GREP = "GREP"
    SWITCH = "SWITCH"
    LOAD = "LOAD"
    SAVE = "SAVE"
    PRINT = "PRINT"
    ESCAPE = "ESCAPE"

    REMOVE_ELEMENTS = "REMOVE ELEMENTS"
    ADD_ELEMENTS = "ADD ELEMENTS"

    @staticmethod
    def parse(s: str):
        s = s.replace("remove elements", ' ')
        s = s.replace("add elements", ' ')

        elems = s.split()
        return elems

    @staticmethod
    def from_str(s: str):
        s = s.strip()
        s = s.upper()

        match s:
            case "ADD USER":
                return Command.ADD_USER
            case "ADD":
                return Command.ADD
            case "REMOVE":
                return Command.REMOVE
            case "FIND":
                return Command.FIND
            case "LIST":
                return Command.LIST
            case "GREP":
                return Command.GREP
            case "SWITCH":
                return Command.SWITCH
            case "LOAD":
                return Command.LOAD
            case "SAVE":
                return Command.SAVE
            case "PRINT":
                return Command.PRINT
            case "ESCAPE":
                return Command.ESCAPE
            case _:

                if s.startswith("REMOVE ELEMENTS"):
                    return Command.REMOVE_ELEMENTS

                if s.startswith("ADD ELEMENTS"):
                    return Command.ADD_ELEMENTS

                else:

                    raise ValueError


def command_input():
    try:
        inp = input("Enter command: ")
        return Command.from_str(inp), inp
    except ValueError:
        print("Not correct input. Try again")
        return command_input()


def pos_int_input(message="Enter integer number: "):
    try:
        value = int(input(message))
        if value <= 0:
            return pos_int_input(message)
        else:
            return value
    except ValueError:
        return pos_int_input(message)


def non_empty_input(message="Enter value: "):
    inp = input(message)

    return inp if inp != "" else non_empty_input(message)