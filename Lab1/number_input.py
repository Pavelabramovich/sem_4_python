def type_input(typ: type, mes="value"):
    try:
        return typ(input(f"Enter the {typ} {mes}: "))
    except ValueError:
        print("Uncorrected input. Try again")
        return type_input(typ)


def pos_int_input(mes="value"):
    n = type_input(int, mes)

    if n >= 0:
        return n
    else:
        print("Uncorrected input. Try again")
        return pos_int_input()


def list_input(typ: type):
    n = pos_int_input("list length")
    return [type_input(typ) for i in range(n)]
