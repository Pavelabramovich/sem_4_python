import re

from input import non_empty_input
from input import command_input
from collection_command import Command

from collection import UserCollections


if __name__ == '__main__':
    first_user_name = non_empty_input("Enter first user name: ")

    with open("data_file.json", 'r+') as file:
        uc = UserCollections(first_user_name, file)

    first_time = True

    while True:
        command, args = command_input(command_list=first_time)
        first_time = False

        match command:
            case Command.ADD_USER:
                if not args:
                    print("No args with command")
                    continue

                new_user_name = args[0]
                uc.add_user(new_user_name)

            case Command.ADD:
                if not args:
                    print("No args with command")
                    continue

                elements = args
                for elem in elements:
                    uc.add_elem(elem)

            case Command.REMOVE:
                if not args:
                    print("No args with command")
                    continue

                elements = args

                absent_elements = []

                for elem in elements:
                    try:
                        uc.remove_elem(elem)
                    except KeyError:
                        absent_elements.append(str(elem))

                print(f"No such elements: {','.join(absent_elements)}")

            case Command.FIND:
                if not args:
                    print("No args with command")
                    continue

                elem = args[0]
                elem = uc.find_elem(elem)

                if elem:
                    print(elem)
                else:
                    print(f"No such element: {elem}")

            case Command.LIST:
                print(uc.get_collection())

            case Command.GREP:
                if not args:
                    print("No args with command")
                    continue

                pattern = args[0]
                try:
                    elements = uc.parse_elem(pattern)

                    if elements:
                        print(','.join([str(e) for e in elements]))
                    else:
                        print("No such elements")

                except re.error as error:
                    print(error)

            case Command.SWITCH:
                is_save = non_empty_input("Do you want save collection (yes/no)? ").lower().strip()

                if is_save == "yes":
                    uc.save_collection()

                user_name = non_empty_input("Enter user name: ")
                uc.switch_user(user_name)

            case Command.LOAD:
                uc.load_collection()

                with open("data_file.json", 'r') as file:
                    uc.load_users(file)

            case Command.SAVE:
                uc.save_collection()

                with open("data_file.json", 'w') as file:
                    uc.save_users(file)

            case Command.PRINT:
                print(str(uc))

            case Command.ESCAPE:
                is_save = non_empty_input("Do you want save collection (yes/no)? ").lower().strip()

                if is_save == "yes":
                    uc.save_collection()

                break

            case _:
                print("Unknown command")
