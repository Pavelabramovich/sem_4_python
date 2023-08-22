from enum import Enum

from SerializationOfClassesAndFuncs.json_serializer import JsonSerializer
from SerializationOfClassesAndFuncs.xml_serializer import XmlSerializer


class SerializerType(Enum):
    JSON = JsonSerializer
    XML = XmlSerializer


class SerializersFactory:
    @staticmethod
    def create_serializer(st: SerializerType | str):
        if isinstance(st, SerializerType):
            return st.value()
        elif isinstance(st, str):
            try:
                return SerializerType[st.strip().upper()].value()
            except KeyError as error:
                raise ValueError(f"Incorrect argument: {st}") from error
        else:
            raise ValueError(f"Incorrect argument: {st}")
