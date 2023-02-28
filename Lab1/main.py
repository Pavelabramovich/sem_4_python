from hello_world import print_hello_world
from operations import operation
from even_list import parse_even
from number_input import type_input
from number_input import list_input

if __name__ == "__main__":
    # 1 task
    print()

    print_hello_world()
    
    # 2 task
    print()

    x = type_input(float)
    y = type_input(float)
    op = input("Input operation ")

    try:
        print(f"Answer is {operation(x, y, op)}")
    except NotImplementedError:
        print(f"Not implemented operation")
    except ZeroDivisionError:
        print(f"Division by zero")

    # 3 task
    print()

    int_lst = list_input(int)
    print(f"Answer is {parse_even(int_lst)}")

