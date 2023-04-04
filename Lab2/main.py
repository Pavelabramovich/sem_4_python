from parse import sentences_count
from parse import non_declarative_sentences_count
from parse import average_sentence_length
from parse import average_word_length
from parse import sub_sentences_top

from input import non_empty_input
from input import command_input
from input import Command
from input import pos_int_input

from collection import UserCollections

if __name__ == '__main__':
    text = non_empty_input("Enter the text to analiz: ")
    try:
        print("Sentence count: ", sentences_count(text))
        print("Non declarative sentence count: ", non_declarative_sentences_count(text))
        print("Average sentence length: ", average_sentence_length(text))
        print("Average word length: ", average_word_length(text))

        k = pos_int_input("Enter top size: ")
        n = pos_int_input("Enter subsentence length: ")
        print("Top subsentence: ", sub_sentences_top(text, k, n))

    except ZeroDivisionError:
        print("Text has no sentences")

    first_user_name = non_empty_input("Enter first user name: ")
    uc = UserCollections(first_user_name)

    desc = """
    Commands:
    ADD USER
    ADD ELEMENT
    REMOVE_ELEMENT
    FIND
    LIST 
    GREP 
    SWITCH   
    LOAD COLLECTION
    SAVE COLLECTION
    PRINT USER LIST
    ESCAPE
    
    """

    print(desc)

    while True:

        command = command_input()

        s = command[1]
        command = command[0]

        match command:
            case Command.ADD_USER:
                new_user_name = non_empty_input("Enter new user name: ")
                uc.add_user(new_user_name)

            case Command.ADD:
                elem = non_empty_input("Enter new element: ")
                uc.add_elem(elem)

            case Command.REMOVE:
                elem = non_empty_input("Enter removing element: ")
                uc.remove_elem(elem)

            case Command.FIND:
                elem = non_empty_input("Enter element to find: ")
                elements = uc.find_elem(elem)

                if elements:
                    for e in elements:
                        print(e)
                else:
                    print("No such elements")

            case Command.LIST:
                print(uc.get_collection())

            case Command.GREP:
                pattern = non_empty_input("Enter regex to parse: ")
                elements = uc.parse_elem(pattern)

                if elements:
                    for e in elements:
                        print(e)
                else:
                    print("No such elements")

            case Command.SWITCH:
                is_save = non_empty_input("Do you want save collection (yes/no)? ").lower().strip()

                if is_save == "yes":
                    uc.save_collection()

                user_name = non_empty_input("Enter user name: ")
                uc.switch_user(user_name)

            case Command.LOAD:
                uc.load_collection()
                uc.load_users()

            case Command.SAVE:
                uc.save_collection()
                uc.save_users()

            case Command.PRINT:
                print(uc.__str__())

            case Command.REMOVE_ELEMENTS:
                elems = Command.parse(s)

                for e in elems:
                    uc.remove_elem(e)

            case Command.ADD_ELEMENTS:
                elems = Command.parse(s)

                for e in elems:
                    uc.add_elem(e)

            case Command.ESCAPE:
                is_save = non_empty_input("Do you want save collection (yes/no)? ").lower().strip()

                if is_save == "yes":
                    uc.save_collection()

                break

            case _:
                print("Unknown command")
