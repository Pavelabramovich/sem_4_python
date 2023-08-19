from print_hello_world import print_hello_world
from get_evens import get_evens
from input import type_input
from input import operation_input
from input import list_input

if __name__ == "__main__":
    # 1 task
    print()

    print_hello_world()
    
    # 2 task
    print()

    x = type_input(float)
    y = type_input(float)
    operation = operation_input()

    try:
        print(f"Answer is {operation.value(x, y)}")
    except ZeroDivisionError:
        print(f"Division by zero")

    # 3 task
    print()

    int_lst = list_input(int, ',')
    ans = get_evens(int_lst)

    if ans:
        print(f"Answer is: {ans}")
    else:
        print("There are no even numbers in the list")

