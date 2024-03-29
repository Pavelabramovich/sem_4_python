import copy
import re
from json import JSONEncoder

import json


class Collection:
    def __init__(self, *args):
        self._elements = set(args)

    def add(self, element, *args):
        self._elements.update([element, *args])

    def __add__(self, other: 'Collection'):
        return Collection(*self._elements, *other._elements)

    def __iadd__(self, other: 'Collection'):
        self.add(*other._elements)
        return self

    def remove(self, element):
        try:
            self._elements.remove(element)
        except KeyError as error:
            raise KeyError("No such element in Collection.") from error

    def find(self, element, *args):
        return [self._elements & {element, *args}]

    def grep(self, pattern: str):
        try:
            return [e for e in self._elements if re.fullmatch(pattern, str(e))]
        except re.error as error:
            raise re.error("Incorrect regex") from error

    def __contains__(self, element):
        return element in self._elements

    def __bool__(self):
        return bool(self._elements)

    def __str__(self):
        return f"<Collection object: {self._elements}>"

    def __copy__(self):
        return Collection(*self._elements)

    def items(self):
        return [*self._elements]


class UserCollections:
    def __init__(self, first_user_name, file):
        self.__users = {first_user_name: Collection()}
        self.__current_user = first_user_name
        self.__current_collection = self.__users[first_user_name]
        file.truncate()

    def add_user(self, user_name: str):
        if user_name not in self.__users.keys():
            self.__users[user_name] = Collection()

    def switch_user(self, user_name: str):
        self.add_user(user_name)

        self.__current_user = user_name
        self.__current_collection = Collection()

    def save_collection(self):
        if self.__current_user:
            self.__users[self.__current_user] += self.__current_collection

    def load_collection(self):
        if self.__current_user:
            self.__current_collection += self.__users[self.__current_user]

    def save_users(self, file):
        json.dump(self, file, cls=UserCollectionEncoder, indent=4)

    def load_users(self, file):
        self.__users = json.load(file, object_hook=from_json)

    def add_elem(self, element):
        self.__current_collection.add(element)

    def remove_elem(self, element):
        self.__current_collection.remove(element)

    def find_elem(self, element):
        if elem := self.__current_collection.find(element):
            return elem[0]
        else:
            return None

    def parse_elem(self, pattern):
        return self.__current_collection.grep(pattern)

    def get_users(self):
        return copy.copy(self.__users)

    def get_collection(self):
        return self.__current_collection.__copy__()

    def __str__(self):
        return str({item[0]: str(item[1]) for item in self.__users.items()})


class UserCollectionEncoder(JSONEncoder):
    def default(self, obj):
        return {item[0]: item[1].items() for item in obj.get_users().items()}


def from_json(uc_dict: dict):
    new_dict = {item[0]: Collection(*item[1]) for item in uc_dict.items()}
    return new_dict
