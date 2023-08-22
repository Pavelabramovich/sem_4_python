import re

import regex
from SerializationOfClassesAndFuncs import BaseSerializer
from SerializationOfClassesAndFuncs import DictSerializer

from SerializationOfClassesAndFuncs.type_constants import nonetype


class XmlSerializer(BaseSerializer):
    NULL_LITERAL = "null"

    KEY_LITERAL = "key"
    VALUE_LITERAL = "value"
    KVPAIR_LITERAL = "kvpair"

    TAG_GROUP_NAME = "tag"
    VALUE_GROUP_NAME = "value"

    XML_SCHEME_SOURCE = ("xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "
                         + "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"")

    XML_SCHEME_PATTERN = XML_SCHEME_SOURCE.replace('.', r'\.')

    ELEMENTARY_NAMES_PATTERN = '|'.join(tuple(t.__name__ for t in (int, float, bool, str, list, dict)))
    TAGS_PATTERN = f"{ELEMENTARY_NAMES_PATTERN}|{NULL_LITERAL}|{KEY_LITERAL}|{VALUE_LITERAL}|{KVPAIR_LITERAL}"

    EMPTY_XML_ELEMENT_PATTERN = fr"<(?P<{TAG_GROUP_NAME}>{TAGS_PATTERN})/>"

    NOT_EMPTY_XML_ELEMENT_PATTERN = (fr"<(?P<{TAG_GROUP_NAME}>{TAGS_PATTERN})>"
                                     + fr"(?P<{VALUE_GROUP_NAME}>([^<>]*)|(?R)+)</(?:{TAGS_PATTERN})>")

    EMPTY_FIRST_XML_ELEMENT_PATTERN = fr"<(?P<{TAG_GROUP_NAME}>{TAGS_PATTERN})\s{XML_SCHEME_PATTERN}/>"

    NOT_EMPTY_FIRST_XML_ELEMENT_PATTERN = (
        fr"<(?P<{TAG_GROUP_NAME}>{TAGS_PATTERN})\s{XML_SCHEME_PATTERN}>"
        + fr"(?P<{VALUE_GROUP_NAME}>((<(?:{TAGS_PATTERN})>"
        + fr"(([^<>]*)|(?4)+)(?# 4 is the index of the value-group in which the search will continue)"
        + fr"</(?:{TAGS_PATTERN})>)|(<(?:{TAGS_PATTERN})/>))*)"
        + fr"</(?:{TAGS_PATTERN})>"
    )

    XML_ELEMENT_PATTERN = fr"({NOT_EMPTY_XML_ELEMENT_PATTERN}|{EMPTY_XML_ELEMENT_PATTERN})"
    FIRST_XML_ELEMENT_PATTERN = fr"({NOT_EMPTY_FIRST_XML_ELEMENT_PATTERN}|{EMPTY_FIRST_XML_ELEMENT_PATTERN})"

    def dumps(self, obj) -> str:
        obj = DictSerializer.to_dict(obj)
        return self.__dumps_from_dict(obj, is_first=True)

    def __dumps_from_dict(self, obj, is_first=False) -> str:
        obj_type = type(obj)

        if obj_type in (int, float, bool):
            return self._create_xml_element(type(obj).__name__, str(obj), is_first)

        if obj is None:
            return self._create_xml_element(self.NULL_LITERAL, '', is_first)

        if obj_type is str:
            data = self._mask_symbols(obj)
            return self._create_xml_element(str.__name__, data, is_first)

        if obj_type is list:
            data = ''.join([self.__dumps_from_dict(o) for o in obj])
            return self._create_xml_element(list.__name__, data, is_first)

        if obj_type is dict:
            data = ''.join(
                [self._create_key_value_pair(key, value) for key, value in obj.items()])
            return self._create_xml_element(dict.__name__, data, is_first)

        else:
            raise ValueError(f"Unknown type: {type(obj)}")

    def _create_key_value_pair(self, key, value):
        # If the type is a string, then no additional tags need to be created.
        if type(key) is str:
            key = self._mask_symbols(key)
        else:
            key = self.__dumps_from_dict(key)

        if type(value) is str:
            value = self._mask_symbols(value)
        else:
            value = self.__dumps_from_dict(value)

        key = self._create_xml_element(self.KEY_LITERAL, key)
        value = self._create_xml_element(self.VALUE_LITERAL, value)

        return self._create_xml_element(self.KVPAIR_LITERAL, f"{key}{value}")

    def loads(self, string: str):
        obj = self._loads_to_dict(string, is_first=True)
        return DictSerializer.from_dict(obj)

    def _loads_to_dict(self, string: str, is_first=False):
        string = string.strip()

        xml_element_pattern = self.FIRST_XML_ELEMENT_PATTERN if is_first else self.XML_ELEMENT_PATTERN

        match = regex.fullmatch(xml_element_pattern, string)

        if match:
            key = match.group(self.TAG_GROUP_NAME)
            value = match.group(self.VALUE_GROUP_NAME) or ''

        else:
            raise ValueError(f"Incorrect format")

        if key == int.__name__:
            return int(value)

        if key == float.__name__:
            return float(value)

        if key == bool.__name__:
            return value == str(True)

        if key == str.__name__:
            return self._unmask_symbols(value)

        if key == self.NULL_LITERAL:
            return None

        if key == list.__name__:
            matches = regex.findall(self.XML_ELEMENT_PATTERN, value)
            return [self._loads_to_dict(match[0]) for match in matches]

        if key == self.KVPAIR_LITERAL:
            key, value = regex.findall(self.XML_ELEMENT_PATTERN, value)

            key = self._loads_to_dict(key[0])
            value = self._loads_to_dict(value[0])

            return key, value

        if key in (self.KEY_LITERAL, self.VALUE_LITERAL):
            match = regex.findall(self.XML_ELEMENT_PATTERN, value)

            # If there are no tags inside the kvpair, then this is a string value.
            if match:
                return self._loads_to_dict(match[0][0])
            else:
                return value

        if key == dict.__name__:
            matches = regex.findall(self.XML_ELEMENT_PATTERN, value)
            kvpairs = tuple(self._loads_to_dict(match[0]) for match in matches)
            return {key: value for key, value in kvpairs}

        else:
            raise ValueError(f"Unknown type: {key}")

    @classmethod
    def _create_xml_element(cls, name: str, data: str, is_first=False):
        if not data or data.isspace():
            if is_first:
                return f"<{name} {cls.XML_SCHEME_SOURCE}/>"
            else:
                return f"<{name}/>"
        else:
            if is_first:
                return f"<{name} {cls.XML_SCHEME_SOURCE}>{data}</{name}>"
            else:
                return f"<{name}>{data}</{name}>"

    @staticmethod
    def _mask_symbols(string: str) -> str:
        return string.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;"). \
            replace('"', "&quot;").replace("'", "&apos;")

    @staticmethod
    def _unmask_symbols(string: str) -> str:
        return string.replace("&amp;", '&').replace("&lt;", '<').replace("&gt;", '>'). \
            replace("&quot;", '"').replace("&apos;", "'")
