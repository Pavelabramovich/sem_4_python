from collection_command import Command


def command_input(command_list=True):
    try:
        all_operations = ','.join([op.name for op in Command])
        if command_list:
            inp = input(f"Enter one of the following command ({all_operations}):")
        else:
            inp = input("Enter a command:")
        return Command.parse(inp)
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
    return input(message) or non_empty_input(message)
