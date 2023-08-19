from enum import Enum


class Command(Enum):
    ADD = "ADD"
    REMOVE = "REMOVE"
    FIND = "FIND"
    LIST = "LIST"
    GREP = "GREP"
    SWITCH = "SWITCH"
    LOAD = "LOAD"
    SAVE = "SAVE"
    PRINT = "PRINT"
    ADD_USER = "ADD USER"
    ESCAPE = "ESCAPE"

    @staticmethod
    def parse(string: str):
        string = string.strip()
        splitted_string = string.split()

        if not splitted_string:
            raise ValueError("There is no command.")

        command, *command_args = splitted_string
        command = command.upper()

        try:
            return Command[command], command_args
        except KeyError as error:
            raise ValueError("Unknown command.") from error
