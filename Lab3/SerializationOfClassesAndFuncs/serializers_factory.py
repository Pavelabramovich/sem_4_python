from enum import Enum

from SerializationOfClassesAndFuncs.base_serializer import BaseSerializer
from SerializationOfClassesAndFuncs.json_serializer import JsonSerializer
from SerializationOfClassesAndFuncs.xml_serializer import XmlSerializer


class Serialization(Enum):
    JSON = JsonSerializer
    XML = XmlSerializer


class SerializersFactory:
    @staticmethod
    def create_serializer(st: Serialization | str) -> BaseSerializer:
        if isinstance(st, Serialization):
            return st.value()
        elif isinstance(st, str):
            try:
                return Serialization[st.strip().upper()].value()
            except KeyError as error:
                raise ValueError(f"Incorrect argument: {st}") from error
        else:
            raise ValueError(f"Incorrect argument: {st}")
