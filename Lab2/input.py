from enum import Enum


def non_empty_input(message="Enter value: "):
    inp = input(message)

    return inp if inp != "" else non_empty_input(message)


class Command(Enum):
    ADD_USER = 0
    ADD_ELEMENT = 1
    REMOVE_ELEMENT = 2
    FIND = 3
    LIST = 4
    GREP = 5
    SWITCH = 6
    LOAD_COLLECTION = 7
    SAVE_COLLECTION = 8
    SAVE_TO_FILE = 9
    LOAD_FROM_FILE = 10
    PRINT_USER_LIST = 11
    ESCAPE = 12

    @staticmethod
    def from_str(s: str):
        s = s.strip()
        s = s.upper()

        match s:
            case "ADD USER":
                return Command.ADD_USER
            case "ADD ELEMENT":
                return Command.ADD_ELEMENT
            case "REMOVE_ELEMENT":
                return Command.REMOVE_ELEMENT
            case "FIND":
                return Command.FIND
            case "LIST":
                return Command.LIST
            case "GREP":
                return Command.GREP
            case "SWITCH":
                return Command.SWITCH
            case "LOAD COLLECTION":
                return Command.LOAD_COLLECTION
            case "SAVE COLLECTION":
                return Command.SAVE_COLLECTION
            case "SAVE TO FILE":
                return Command.SAVE_TO_FILE
            case "LOAD FROM FILE":
                return Command.LOAD_FROM_FILE
            case "PRINT USER LIST":
                return Command.PRINT_USER_LIST
            case "ESCAPE":
                return Command.ESCAPE
            case _:
                raise ValueError


def command_input():
    try:
        inp = input("Enter command: ")
        return Command.from_str(inp)
    except ValueError:
        print("Not correct input. Try again")
        return command_input()


def pos_int_input(message = "Enter integer number: "):
    try:
        value = int(input(message))
        if value <= 0:
            return pos_int_input(message)
        else:
            return value
    except ValueError:
        return  pos_int_input(message)

