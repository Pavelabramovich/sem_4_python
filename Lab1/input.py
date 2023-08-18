from operations import Operation


def type_input(typ: type, value="value"):
    try:
        return typ(input(f"Enter the {typ.__name__} {value}: "))
    except ValueError:
        print("Uncorrected input. Try again")
        return type_input(typ)


def pos_int_input(value="value"):
    n = type_input(int, value)

    if n >= 0:
        return n
    else:
        print("Uncorrected input. Try again")
        return pos_int_input()


def operation_input(value="value"):
    try:
        all_operations = ','.join([op.name for op in Operation])
        str_operation = input(f"Enter the one of the following operations ({all_operations}) ").upper()
        return Operation[str_operation]
    except (ValueError, KeyError):
        print("Uncorrected input. Try again")
        return operation_input(value)


def list_input(typ: type, sep: str):
    lst = input(f"Enter a list of {typ.__name__}s using '{sep}' as separator:")

    try:
        return [typ(value) for value in lst.split(sep)]
    except ValueError:
        print("Uncorrected input. Try again")
        return list_input(typ, sep)
