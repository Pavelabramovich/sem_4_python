import inspect
from SerializationOfClassesAndFuncs.type_constants import (
    nonetype, moduletype, codetype, celltype,
    functype, smethodtype, cmethodtype, proptype,
    mapproxytype, gentype, ellipsistype, notimplementedtype,
    uniontype, genaliastype,
    CODE_PROPERTIES, DESCRIPTOR_TYPES, BUILTINS,
    DICT_OPERATIONS_TYPES, ITER_TYPES
)

from inspect import isfunction, ismethod
from datetime import date, time, datetime, timedelta
from math import inf, isnan


class DictSerializer:
    # All elementary python types steal be elementary.
    # Complex types will be represented as dicts and lists.
    # To get rid of the circular reference issues, all serialized objects are
    # placed in a dictionary with its id as the key. Then, if an object is encountered that has already
    # been met, it will be serialized as a reference. During deserialization, such a dictionary will be created,
    # while at the same time, normal fields will be restored first, and only after the objects are completely
    # formed, a second traversal will be performed with the replacement of the recursive reference to
    # already existing objects. This will not create recursive references to immutable types.
    # Instead, links to their fields will be created.

    TYPE_KW = "type"
    SOURCE_KW = "source"
    ID_KW = "id"

    RECURSION_KW = "__recursion__"

    CODE_KW = "__code__"
    GLOBALS_KW = functype.__globals__.__name__
    NAME_KW = "__name__"
    DEFAULTS_KW = "__defaults__"
    CLOSURE_KW = functype.__closure__.__name__

    BASES_KW = "__bases__"
    DICT_KW = "__dict__"

    CLASS_KW = "__class__"

    BUILTIN_KW = "__builtin__"

    @classmethod
    def to_dict(cls, obj):
        return cls._to_dict(obj)

    @classmethod
    def _update_serialize_recursion_dict(cls, obj, recursion_dict):
        type_name = type(obj).__name__
        if type_name in recursion_dict:
            recursion_dict[type_name].update({id(obj)})
        else:
            recursion_dict[type_name] = {id(obj)}

    @classmethod
    def _is_obj_in_serialize_recursion_dict(cls, obj, recursion_dict):
        type_name = type(obj).__name__
        if type_name in recursion_dict:
            return id(obj) in recursion_dict[type_name]
        else:
            return False

    @classmethod
    def _to_dict(cls, obj, recursion_dict=None, recursion_protection=True):
        obj_type = type(obj)

        if obj_type in (int, bool, str, nonetype):
            return obj

        if obj_type is float:
            if obj in (inf, -inf) or isnan(obj):
                return {cls.TYPE_KW: float.__name__,
                        cls.SOURCE_KW: str(obj)}
            else:
                return obj

        elif obj_type is complex:
            return {cls.TYPE_KW: complex.__name__,
                    cls.SOURCE_KW: {complex.real.__name__: cls._to_dict(obj.real),
                                    complex.imag.__name__: cls._to_dict(obj.imag)}}

        elif obj_type is ellipsistype:
            return {cls.TYPE_KW: ellipsistype.__name__}

        elif obj_type is notimplementedtype:
            return {cls.TYPE_KW: notimplementedtype.__name__}

        elif obj_type in (set, tuple, frozenset, bytes, bytearray, gentype):
            return {cls.TYPE_KW: obj_type.__name__,
                    cls.SOURCE_KW: cls._to_dict([*obj], recursion_dict, recursion_protection=False)}

        elif obj_type is date:
            return {cls.TYPE_KW: date.__name__,
                    cls.SOURCE_KW: {date.day.__name__: obj.day,
                                    date.month.__name__: obj.month,
                                    date.year.__name__: obj.year}}

        elif obj_type is time:
            return {cls.TYPE_KW: time.__name__,
                    cls.SOURCE_KW: {time.hour.__name__: obj.hour,
                                    time.minute.__name__: obj.minute,
                                    time.second.__name__: obj.second,
                                    time.microsecond.__name__: obj.microsecond}}

        elif obj_type is datetime:
            return {cls.TYPE_KW: datetime.__name__,
                    cls.SOURCE_KW: {datetime.date.__name__: cls._to_dict(obj.date(), recursion_dict),
                                    datetime.time.__name__: cls._to_dict(obj.time(), recursion_dict)}}

        elif obj_type is timedelta:
            return {cls.TYPE_KW: timedelta.__name__,
                    cls.SOURCE_KW: {timedelta.days.__name__: obj.days,
                                    timedelta.seconds.__name__: obj.seconds,
                                    timedelta.microseconds.__name__: obj.microseconds}}

        elif obj_type in ITER_TYPES:
            return cls._to_dict((i for i in obj), recursion_dict, recursion_protection=False)

        elif obj_type in DICT_OPERATIONS_TYPES:
            return cls._to_dict(tuple((i for i in obj)), recursion_dict, recursion_protection=False)

        elif obj_type is uniontype:
            return {cls.TYPE_KW: uniontype.__name__,
                    cls.SOURCE_KW: cls._to_dict(obj.__args__, recursion_dict, recursion_protection=False)}

        elif obj_type is genaliastype:
            origin = cls._to_dict(obj.__origin__, recursion_dict)
            args = cls._to_dict(obj.__args__, recursion_dict, recursion_protection=False)

            return {cls.TYPE_KW: genaliastype.__name__,
                    cls.SOURCE_KW: {genaliastype.__origin__.__name__: origin,
                                    genaliastype.__args__.__name__: args}}

        elif obj_type is celltype:
            return {cls.TYPE_KW: celltype.__name__,
                    cls.SOURCE_KW: cls._to_dict(obj.cell_contents, recursion_dict)}

        elif obj in BUILTINS.values():
            return {cls.TYPE_KW: cls.BUILTIN_KW,
                    cls.SOURCE_KW: obj.__name__}

        if recursion_dict is None:
            recursion_dict = {}

        if recursion_protection:
            if cls._is_obj_in_serialize_recursion_dict(obj, recursion_dict):
                return {cls.TYPE_KW: cls.RECURSION_KW,
                        cls.SOURCE_KW: {cls.TYPE_KW: obj_type.__name__,
                                        cls.ID_KW: cls._to_dict(id(obj))}}
            else:
                cls._update_serialize_recursion_dict(obj, recursion_dict)

        if obj_type is list:
            if recursion_protection:
                ser_obj = {cls.TYPE_KW: list.__name__,
                           cls.SOURCE_KW: cls._to_dict(obj, recursion_dict, recursion_protection=False)}
            else:
                return [cls._to_dict(o, recursion_dict) for o in obj]

        elif obj_type is set:
            return {cls.TYPE_KW: obj_type.__name__,
                    cls.SOURCE_KW: cls._to_dict([*obj], recursion_dict, recursion_protection=False)}

        elif obj_type is dict:
            # Since the key in the dictionary can be a hashable object, which will be represented as a non-hashable
            # dictionary, it is easier to represent the dictionary as a list of key-value pairs
            ser_obj = {cls.TYPE_KW: dict.__name__,
                       cls.SOURCE_KW: [[cls._to_dict(key, recursion_dict), cls._to_dict(value, recursion_dict)]
                                       for key, value in obj.items()]}

        elif obj_type is moduletype:
            ser_obj = {cls.TYPE_KW: moduletype.__name__,
                       cls.SOURCE_KW: obj.__name__}

        elif obj_type is codetype:
            code = {cls.TYPE_KW: codetype.__name__}
            source = {}

            for (key, value) in inspect.getmembers(obj):
                if key in CODE_PROPERTIES:
                    source[key] = cls._to_dict(value, recursion_dict, recursion_protection=False)

            code.update({cls.SOURCE_KW: source})
            ser_obj = code

        elif obj_type in (smethodtype, cmethodtype):
            ser_obj = {cls.TYPE_KW: obj_type.__name__,
                       cls.SOURCE_KW: cls._to_dict(obj.__func__, recursion_dict)}

        elif obj_type is proptype:
            fget = cls._to_dict(obj.fget, recursion_dict)
            fset = cls._to_dict(obj.fset, recursion_dict)
            fdel = cls._to_dict(obj.fdel, recursion_dict)

            ser_obj = {cls.TYPE_KW: proptype.__name__,
                       cls.SOURCE_KW: {proptype.fget.__name__: fget,
                                       proptype.fset.__name__: fset,
                                       proptype.fdel.__name__: fdel}}

        elif isfunction(obj) or ismethod(obj):
            source = {}

            # Code
            source[cls.CODE_KW] = cls._to_dict(obj.__code__, recursion_dict)

            # Global vars
            source[cls.GLOBALS_KW] = {cls._to_dict(key, recursion_dict): cls._to_dict(value, recursion_dict)
                                      for key, value in cls._get_gvars(obj).items()}

            # Name
            source[cls.NAME_KW] = cls._to_dict(obj.__name__)

            # Defaults
            source[cls.DEFAULTS_KW] = cls._to_dict(obj.__defaults__, recursion_dict)

            # Closure
            source[cls.CLOSURE_KW] = cls._to_dict(obj.__closure__, recursion_dict)

            ser_obj = {cls.TYPE_KW: functype.__name__,
                       cls.SOURCE_KW: source}

        elif inspect.isclass(obj):
            source = {}

            # Name
            source[cls.NAME_KW] = cls._to_dict(obj.__name__)

            # Bases
            source[cls.BASES_KW] = cls._to_dict(tuple(b for b in obj.__bases__ if b is not object))

            # Dict
            source[cls.DICT_KW] = {cls._to_dict(key, recursion_dict): cls._to_dict(value, recursion_dict)
                                   for key, value in cls._get_obj_dict(obj).items()}

            ser_obj = {cls.TYPE_KW: type.__name__,
                       cls.SOURCE_KW: source}

        elif isinstance(obj, object):
            source = {}

            # Class
            source[cls.CLASS_KW] = cls._to_dict(obj.__class__, recursion_dict=recursion_dict)

            # Dict
            source[cls.DICT_KW] = {cls._to_dict(key, recursion_dict): cls._to_dict(value, recursion_dict)
                                   for key, value in cls._get_obj_dict(obj).items()}

            return {cls.TYPE_KW: object.__name__,
                    cls.SOURCE_KW: source}

        else:
            raise ValueError(f"Unknown type: {obj_type}")

        if recursion_protection:
            ser_obj.update({cls.ID_KW: id(obj)})

        return ser_obj

    @staticmethod
    def _get_gvars(func):
        gvars = {}

        for gvar_name in func.__code__.co_names:
            # Separating the variables that the function needs
            if gvar_name in func.__globals__:
                gvars[gvar_name] = func.__globals__[gvar_name]

        return gvars

    @staticmethod
    def _get_obj_dict(obj):
        dct = {}

        if hasattr(obj, '__dict__'):
            for key, value in obj.__dict__.items():
                if type(value) not in DESCRIPTOR_TYPES:
                    dct[key] = value

        return dct

    class __RecursionWrapper:
        def __init__(self, obj_type, obj_id):
            self.obj_type = obj_type
            self.obj_id = obj_id

    class __ObjectWrapper:
        def __init__(self, dct, cls_rec_wrapper):
            self.dct = dct
            self.cls_rec_wrapper = cls_rec_wrapper

    @classmethod
    def _update_deserialization_recursion_dict(cls, deser_obj, recursion_id, recursion_dict):
        type_name = type(deser_obj).__name__
        if type_name in recursion_dict:
            recursion_dict[type_name].update({recursion_id: deser_obj})
        else:
            recursion_dict[type_name] = {recursion_id: deser_obj}

    @classmethod
    def from_dict(cls, obj):
        recursion_dict = {}
        res = cls._from_dict(obj, recursion_dict)

        return cls._restore_recursion(res, recursion_dict)

    @classmethod
    def _from_dict(cls, obj, recursion_dict=None):
        if type(obj) in (int, float, bool, str, nonetype):
            return obj

        elif type(obj) is list:
            return [cls._from_dict(o, recursion_dict) for o in obj]

        else:
            obj_type = obj[cls.TYPE_KW]

            if obj_type == ellipsistype.__name__:
                return ...

            if obj_type == notimplementedtype.__name__:
                return NotImplemented

            obj_source = obj[cls.SOURCE_KW]

            if obj_type == float.__name__:
                return float(obj_source)

            if obj_type == complex.__name__:
                return (obj_source[complex.real.__name__] +
                        obj_source[complex.imag.__name__] * 1j)

            elif obj_type in (cols_dict := {t.__name__: t for t in (set, frozenset, tuple, bytes, bytearray)}):
                return cols_dict[obj_type](cls._from_dict(obj_source, recursion_dict))

            elif obj_type == uniontype.__name__:
                args = cls._from_dict(obj_source, recursion_dict)

                res = args[0]

                for i in range(1, len(args)):
                    res |= args[i]

                return res

            elif obj_type == genaliastype.__name__:
                args = cls._from_dict(obj_source[genaliastype.__args__.__name__], recursion_dict)
                origin = cls._from_dict(obj_source[genaliastype.__origin__.__name__], recursion_dict)

                return origin[args]

            elif obj_type == date.__name__:
                day = obj_source[date.day.__name__]
                month = obj_source[date.month.__name__]
                year = obj_source[date.year.__name__]

                return date(day=day, month=month, year=year)

            elif obj_type == time.__name__:
                hour = obj_source[time.hour.__name__]
                minute = obj_source[time.minute.__name__]
                second = obj_source[time.second.__name__]
                microsecond = obj_source[time.microsecond.__name__]

                return time(hour=hour, minute=minute, second=second, microsecond=microsecond)

            elif obj_type == datetime.__name__:
                d = cls._from_dict(obj_source[datetime.date.__name__])
                t = cls._from_dict(obj_source[datetime.time.__name__])

                return datetime.combine(date=d, time=t)

            elif obj_type == timedelta.__name__:
                days = obj_source[timedelta.days.__name__]
                seconds = obj_source[timedelta.seconds.__name__]
                microseconds = obj_source[timedelta.microseconds.__name__]

                return timedelta(days=days, seconds=seconds, microseconds=microseconds)

            elif obj_type == gentype.__name__:
                lst = cls._from_dict(obj_source, recursion_dict)
                return (i for i in lst)

            elif obj_type == celltype.__name__:
                return celltype(cls._from_dict(obj_source, recursion_dict))

            elif obj_type == cls.BUILTIN_KW:
                return BUILTINS[obj_source]

            elif obj_type == cls.RECURSION_KW:
                return cls.__RecursionWrapper(obj_source[cls.TYPE_KW], obj_source[cls.ID_KW])

            elif obj_type == list.__name__:
                deser_obj = cls._from_dict(obj_source, recursion_dict)

            elif obj_type == dict.__name__:
                deser_obj = {cls._from_dict(key, recursion_dict): cls._from_dict(value, recursion_dict)
                             for key, value in obj_source}

            elif obj_type == moduletype.__name__:
                deser_obj = __import__(obj_source)

            elif obj_type == codetype.__name__:
                deser_obj = codetype(*[cls._from_dict(obj_source[prop], recursion_dict) for prop in CODE_PROPERTIES])

            elif obj_type == smethodtype.__name__:
                deser_obj = smethodtype(cls._from_dict(obj_source, recursion_dict))

            elif obj_type == cmethodtype.__name__:
                deser_obj = cmethodtype(cls._from_dict(obj_source, recursion_dict))

            elif obj_type == proptype.__name__:
                fget = cls._from_dict(obj_source[proptype.fget.__name__], recursion_dict)
                fset = cls._from_dict(obj_source[proptype.fset.__name__], recursion_dict)
                fdel = cls._from_dict(obj_source[proptype.fdel.__name__], recursion_dict)

                deser_obj = proptype(fget=fget, fset=fset, fdel=fdel)

            elif obj_type == functype.__name__:
                code = cls._from_dict(obj_source[cls.CODE_KW], recursion_dict)
                gvars = {cls._from_dict(key, recursion_dict): cls._from_dict(value, recursion_dict)
                         for key, value in obj_source[cls.GLOBALS_KW].items()}
                name = cls._from_dict(obj_source[cls.NAME_KW], recursion_dict)
                defaults = cls._from_dict(obj_source[cls.DEFAULTS_KW], recursion_dict)
                closure = cls._from_dict(obj_source[cls.CLOSURE_KW], recursion_dict)

                deser_obj = functype(code, gvars, name, defaults, closure)

            elif obj_type == type.__name__:
                name = cls._from_dict(obj_source[cls.NAME_KW], recursion_dict)
                bases = cls._from_dict(obj_source[cls.BASES_KW], recursion_dict)
                dct = {cls._from_dict(key, recursion_dict): cls._from_dict(value, recursion_dict)
                       for key, value in obj_source[cls.DICT_KW].items()}

                deser_obj = type(name, bases, dct)

            elif obj_type == object.__name__:
                clas = cls._from_dict(obj_source[cls.CLASS_KW], recursion_dict)
                dct = {cls._from_dict(key, recursion_dict): cls._from_dict(value, recursion_dict)
                       for key, value in obj_source[cls.DICT_KW].items()}

                if type(clas) is cls.__RecursionWrapper:
                    return cls.__ObjectWrapper(dct, clas)

                try:
                    deser_obj = object.__new__(clas)
                except TypeError:
                    deser_obj = clas.__new__(clas)

                deser_obj.__dict__ = dct

            else:
                raise ValueError(f"Unknown type: {obj_type}")

            if obj_id := obj.get(cls.ID_KW, False):
                if recursion_dict is not None:
                    cls._update_deserialization_recursion_dict(deser_obj, obj_id, recursion_dict)

            return deser_obj

    @classmethod
    def _restore_recursion(cls, obj, recursion_dict, restored_dict=None):
        obj_type = type(obj)

        if obj_type is cls.__RecursionWrapper:
            return recursion_dict[obj.obj_type][obj.obj_id]

        if obj_type is cls.__ObjectWrapper:
            clas = cls._restore_recursion(obj.cls_rec_wrapper, recursion_dict, restored_dict)
            dct = cls._restore_recursion(obj.dct, recursion_dict, restored_dict)

            try:
                obj = object.__new__(clas)
            except TypeError:
                obj = clas.__new__(clas)

            obj.__dict__ = dct
            return cls._restore_recursion(obj, recursion_dict, restored_dict)

        if (obj_type in (int, float, bool, complex, str, nonetype, bytes, bytearray, ellipsistype,
                         notimplementedtype, date, time, datetime, timedelta)
            or obj_type in DESCRIPTOR_TYPES
            or obj in BUILTINS.values()):
            return obj

        if obj_type in (set, tuple, frozenset):
            return obj_type([cls._restore_recursion(item, recursion_dict, restored_dict) for item in obj])

        if obj_type is gentype:
            lst = [cls._restore_recursion(item, recursion_dict, restored_dict) for item in obj]
            return (i for i in lst)

        if obj_type is uniontype:
            args = cls._restore_recursion(obj.__args__, recursion_dict, restored_dict)

            res = args[0]

            for i in range(1, len(args)):
                res |= args[i]

            return res

        if obj_type is genaliastype:
            args = cls._restore_recursion(obj.__args__, recursion_dict, restored_dict)
            origin = cls._restore_recursion(obj.__origin__, recursion_dict, restored_dict)

            return origin[args]

        if restored_dict is None:
            restored_dict = {}

        if obj_type.__name__ in restored_dict:
            if id(obj) in restored_dict[obj_type.__name__]:
                return obj
            else:
                restored_dict[obj_type.__name__].update({id(obj)})
        else:
            restored_dict[obj_type.__name__] = {id(obj)}

        if obj_type is list:
            for index, item in enumerate(obj):
                obj[index] = cls._restore_recursion(item, recursion_dict, restored_dict)

        elif obj_type is mapproxytype:
            dct = dict(obj)
            return cls._restore_recursion(dct, recursion_dict, restored_dict)

        elif obj_type is dict:
            for key, value in obj.items():
                new_key = cls._restore_recursion(key, recursion_dict, restored_dict)
                new_value = cls._restore_recursion(value, recursion_dict, restored_dict)

                if new_key is not key:
                    obj[new_key] = obj[key]
                    del obj[key]

                obj[new_key] = new_value

        elif obj_type is codetype:
            for prop in CODE_PROPERTIES:
                cls._restore_recursion(getattr(obj, prop), recursion_dict, restored_dict)

        elif obj_type is celltype:
            obj.cell_contents = cls._restore_recursion(obj.cell_contents, recursion_dict, restored_dict)

        elif obj_type in (smethodtype, cmethodtype):
            cls._restore_recursion(obj.__func__, recursion_dict, restored_dict)

        elif obj_type is proptype:
            cls._restore_recursion(obj.fget, recursion_dict, restored_dict)
            cls._restore_recursion(obj.fset, recursion_dict, restored_dict)
            cls._restore_recursion(obj.fdel, recursion_dict, restored_dict)

        elif isfunction(obj) or ismethod(obj):
            obj.__code__ = cls._restore_recursion(obj.__code__, recursion_dict, restored_dict)
            cls._restore_recursion(obj.__globals__, recursion_dict, restored_dict)
            obj.__defaults__ = cls._restore_recursion(obj.__defaults__, recursion_dict, restored_dict)
            cls._restore_recursion(obj.__closure__, recursion_dict, restored_dict)

        elif isinstance(obj, type):
            new_dict = cls._restore_recursion(obj.__dict__, recursion_dict, restored_dict)
            for key, value in new_dict.items():
                if key != '__dict__':
                    setattr(obj, key, value)

            obj.__bases__ = cls._restore_recursion(obj.__bases__, recursion_dict, restored_dict)

        elif isinstance(obj, object):
            new_dict = cls._restore_recursion(obj.__dict__, recursion_dict, restored_dict)
            for key, value in new_dict.items():
                if key != '__dict__':
                    setattr(obj, key, value)

            obj.__class__ = cls._restore_recursion(obj.__class__, recursion_dict, restored_dict)

        return obj
